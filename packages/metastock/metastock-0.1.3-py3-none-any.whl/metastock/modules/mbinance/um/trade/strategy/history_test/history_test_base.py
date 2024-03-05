import os
from abc import ABC
from datetime import datetime

import arrow
import pandas as pd
import xlsxwriter
from rich.table import Table

from metastock.modules.core.logging.logger import AppLogger, Logger
from metastock.modules.core.util.csv_writer import CsvWriter
from metastock.modules.core.util.dict_deep_merge import dict_deep_merge
from metastock.modules.mbinance.um.db.resources.candlestick_resource import (
    get_candlestick_history_df,
)
from metastock.modules.mbinance.um.exchange.connector.api_data_connector import (
    UMApiDataConnector,
)
from metastock.modules.mbinance.um.trade.strategy.config.strategy_config_base import (
    StrategyConfigBase,
)
from metastock.modules.mbinance.um.value.um_value import UMValue
from metastock.modules.mbinance.value.common import TimeInterval


class HistoryTestBase(ABC):
    NUM_CANDLES_FUTURE_CHECK = (
        20  # Số lượng cây nến sẽ cộng vào endtime để đảm bảo có dữ liệu tính TP/SL
    )

    def __init__(
        self,
        strategy_config: StrategyConfigBase,
        start_time: str,
        interval: TimeInterval = TimeInterval.ONE_MINUTE.value,
        end_time: str = None,
        logger: AppLogger = Logger(),
    ):
        self._strategy_config = strategy_config
        self._start_time = start_time
        self._end_time = end_time
        self._logger = logger
        self._interval = interval

        self.__start_time = None
        self.__end_time = None
        self.__kline = None
        self.__results = []
        self.__calculate_count_data = None
        self.__workbook = None
        self.__worksheet = None
        self.__config_str = str(strategy_config)
        self.__file_path = None

    def __get_file_path(self):
        if self.__file_path is None:
            current_directory = os.getcwd()
            results_folder_path = os.path.join(current_directory, "test_results")
            if not os.path.exists(results_folder_path):
                os.makedirs(results_folder_path)

            origin_filename = f"{UMValue.SYMBOL()}_{self._interval}_{self.get_start_time().format('YYYY-MM-DD')}_{self.get_end_time().format('YYYY-MM-DD')}"

            i = 0
            is_workbook_exists = False
            workbook_path = None
            while workbook_path is None or is_workbook_exists:
                i = i + 1
                filename = f"{origin_filename}_{i}"
                workbook_path = os.path.join(results_folder_path, filename)
                is_workbook_exists = os.path.exists(f"{workbook_path}.xlsx")

            self.__file_path = workbook_path

        return self.__file_path

    def _get_workbook(self):
        if self.__workbook is None:
            self.__workbook = xlsxwriter.Workbook(f"{self.__get_file_path()}.xlsx")

        return self.__workbook

    def _get_worksheet(self):
        if self.__worksheet is None:
            self.__worksheet = self._get_workbook().add_worksheet()

        return self.__worksheet

    def write_results_to_excel(self):
        workbook = self._get_workbook()
        worksheet = self._get_worksheet()

        excel_start_row = 2

        # write header
        header_mapping = {
            "dt": {"index": 0, "width": 10},
            "status": {"index": 1, "width": 10},
            "price": {"index": 2, "width": 12, "format": "float"},
            "price_min": {"index": 3, "width": 12, "format": "float"},
            "price_max": {"index": 4, "width": 12, "format": "float"},
            "price_position": {"index": 5, "width": 12},
            "tp": {"index": 6, "width": 10},
            "cl": {"index": 7, "width": 10},
            "max_tp_price": {"index": 8, "width": 13.5, "format": "float"},
            "max_sl_price": {"index": 9, "width": 13.5, "format": "float"},
            "date": {"index": 10, "width": 12},
        }

        # __________________________________ Format column __________________________________
        for column_name, column_data in header_mapping.items():
            if isinstance(column_data, dict):
                column_index = column_data.get("index")
                column_width = column_data.get(
                    "width", 10
                )  # Mặc định là 10 nếu không được chỉ định
                if column_index is not None:
                    worksheet.set_column(
                        f"{chr(65 + column_index)}:{chr(65 + column_index)}",
                        column_width,
                    )  # Định dạng độ rộng cột
                    # Kiểm tra xem cột có định dạng là số float không
                    # if column_data.get("format") == "float":
                    #     float_format = workbook.add_format({"num_format": "#,##0.00"})
                    #     worksheet.set_column(
                    #         column_index, column_index, None, float_format
                    #     )
        # __________________________________ $$$$ __________________________________

        # write header
        header_format = workbook.add_format(
            {"bold": True, "bg_color": "#F0F0F0", "font_color": "black", "border": 1}
        )

        for column_name, column_data in header_mapping.items():
            column_index = column_data.get("index")
            if column_index is not None:
                worksheet.write(
                    excel_start_row, column_index, column_name, header_format
                )

        # write data for each row
        ignore_data = ["meta"]
        i = 0
        for row in self.__results:
            i += 1
            for column_name, val in row.items():
                if column_name in ignore_data:
                    continue
                cell_format = workbook.add_format()
                if (
                    column_name == "dt" or column_name == "tp" or column_name == "cl"
                ) and val is not None:
                    arrow_obj = arrow.get(val)
                    val = arrow_obj.format("HH:mm")
                    date_str = arrow_obj.format("YYYY-MM-DD")
                    if column_name == "dt":
                        worksheet.write(
                            excel_start_row + i,
                            header_mapping["date"].get("index"),
                            date_str,
                        )

                if column_name == "status":
                    if val == "PASS":
                        cell_format = workbook.add_format(
                            {
                                "bold": True,
                                "bg_color": "#84f542",
                                "font_color": "black",
                                "border": 1,
                            }
                        )
                    elif val == "FAIL":
                        cell_format = workbook.add_format(
                            {
                                "bold": True,
                                "bg_color": "#f54242",
                                "font_color": "black",
                                "border": 1,
                            }
                        )
                if column_name == "price":
                    # Tôi muốn cột này sort được
                    pass

                worksheet.write(
                    excel_start_row + i,
                    header_mapping[column_name].get("index"),
                    val,
                    cell_format,
                )

        # Summary
        # Merge 10 cột đầu tiên từ cột A đến J
        worksheet.merge_range(
            "A1:J1", "Nội dung của merge cells", workbook.add_format({"bold": True})
        )

        # Ghi nội dung vào ô merge
        cal_count_data = self.__calculate_count()
        pass_count, fail_count, unknown_count = cal_count_data[:3]
        worksheet.write(
            "A1",
            f"Pass",
            workbook.add_format({"text_wrap": True, "align": "top"}),
        )
        worksheet.write(
            "A1",
            f"{pass_count}",
            workbook.add_format(
                {"text_wrap": True, "align": "top", "font_color": "green", "bold": True}
            ),
        )
        worksheet.write(
            "A1",
            f"Pass {pass_count} / Fail {fail_count} / Unknown {unknown_count} \n {self.__config_str}",
            workbook.add_format({"text_wrap": True, "align": "top"}),
        )
        worksheet.set_row(0, 180)
        worksheet.freeze_panes(1, 0)
        worksheet.freeze_panes(excel_start_row + 1, 0)

        # end
        workbook.close()

    def _add_to_results(
        self,
        dt: datetime,
        status: str,
        price: float | None,
        price_min: float,
        price_max: float,
        price_position: str | None,
        tp: datetime | None,
        cl: datetime | None,
        max_tp_price: float = None,
        max_sl_price: float = None,
        # additional info
        meta: dict = None,
    ):
        self.__results.append(
            {
                "dt": dt,
                "status": status,
                "price": price,
                "price_min": price_min,
                "price_max": price_max,
                "price_position": price_position,
                "tp": tp,
                "cl": cl,
                "max_tp_price": max_tp_price,
                "max_sl_price": max_sl_price,
                "meta": meta,
            }
        )

    def __calculate_count(self):
        if self.__calculate_count_data is None:
            pass_count = sum(1 for row in self.__results if row["status"] == "PASS")
            fail_count = sum(1 for row in self.__results if row["status"] == "FAIL")
            unknown_count = sum(
                1 for row in self.__results if row["status"] == "UNKNOWN"
            )

            self.__calculate_count_data = [pass_count, fail_count, unknown_count]

        return self.__calculate_count_data

    def _write_to_csv(self):
        df = pd.DataFrame(
            self.__results,
            columns=[
                "dt",
                "status",
                "price",
                "price_min",
                "price_max",
                "price_position",
                "tp",
                "cl",
                "max_tp_price",
                "max_sl_price",
            ],
        )
        df.to_csv(f"{self.__get_file_path()}.csv", index=False)

    def _write_to_cli(self):
        cal_count_data = self.__calculate_count()
        pass_count, fail_count, unknown_count = cal_count_data[:3]
        table = Table(
            title=f"Pass [green b]{pass_count}[/green b] / Fail [red b]{fail_count}[/red b] / Unknown [yellow b]{unknown_count}[/yellow b]"
        )
        table.add_column("Time", justify="right", style="cyan", no_wrap=True)
        table.add_column("Status", style="magenta")
        table.add_column("Price", justify="right", style="green")
        table.add_column("TP", justify="right", style="green")
        table.add_column("CL", justify="right", style="green")
        table.add_column("MAX TP", justify="right", style="green")
        table.add_column("MAX SL", justify="right", style="green")

        def __format_status(status):
            if status == "PASS":
                return "[green]PASS[/green]"
            elif status == "FAIL":
                return "[red]FAIL[/red]"
            elif status == "UNKNOWN":
                return "[yellow]UNKNOWN[/yellow]"

        for row in self.__results:
            table.add_row(
                arrow.get(row["dt"]).format("HH:mm YYYY-MM-DD"),
                __format_status(row["status"]),
                f"{row['price']}({row['price_position']})",
                arrow.get(row["tp"]).format("HH:mm YYYY-MM-DD")
                if row["tp"] is not None
                else "",
                arrow.get(row["cl"]).format("HH:mm YYYY-MM-DD")
                if row["cl"] is not None
                else "",
                f"{row['max_tp_price']}",
                f"{row['max_sl_price']}",
            )

        self.logger().console().print(table, justify="center")
        self.logger().console().print(
            f"[{self._start_time} -> {self._end_time}] Pass [green b]{pass_count}[/green b] / Fail [red b]{fail_count}[/red b] / Unknown [yellow b]{unknown_count}[/yellow b]",
            justify="center",
        )
        self._write_to_csv()
        self._write_results("results")

    def _write_results(self, filename: str):
        current_directory = os.getcwd()
        results_folder_path = os.path.join(current_directory, "test_results/summary")
        if not os.path.exists(results_folder_path):
            os.makedirs(results_folder_path)

        origin_filename = f"{UMValue.SYMBOL()}_{self._interval}_{self.get_start_time().format('YYYY-MM-DD')}_{self.get_end_time().format('YYYY-MM-DD')}"
        file_path = os.path.join(
            results_folder_path, f"{origin_filename}_{filename}.csv"
        )
        csv_writer = CsvWriter(file_path=file_path)

        cal_count_data = self.__calculate_count()
        pass_count, fail_count, unknown_count = cal_count_data[:3]
        profit = (
            pass_count * self._strategy_config.get_tp()
            - fail_count * self._strategy_config.get_sl()
        )

        csv_writer.write_to_csv(
            [
                dict_deep_merge(
                    {
                        "start": self.get_start_time().format("YYYY-MM-DD"),
                        "end": self.get_end_time().format("YYYY-MM-DD"),
                        "pass_count": pass_count,
                        "fail_count": fail_count,
                        "unknown_count": unknown_count,
                        "profit": profit,
                    },
                    {
                        **self._strategy_config.get_config_fields(),
                        "excel_data": self.__get_file_path(),
                    },
                )
            ]
        )

    def logger(self):
        return self._logger

    def get_start_time(self) -> arrow:
        if self.__start_time is None:
            shift_minutes = UMApiDataConnector.KLINE_HISTORY_SIZE
            if self._interval == TimeInterval.THIRTY_MINUTES.value:
                shift_minutes = 30 * UMApiDataConnector.KLINE_HISTORY_SIZE
            self.__start_time = (
                arrow.get(self._start_time, "YYYY-MM-DD HH:mm:SS")
                .shift(minutes=-shift_minutes)
                .replace(tzinfo="Asia/Bangkok")
            )

        return self.__start_time

    def get_end_time(self) -> arrow:
        if self.__end_time is None:
            if self._end_time is None:
                shift_minutes = HistoryTestBase.NUM_CANDLES_FUTURE_CHECK
                if self._interval == TimeInterval.THIRTY_MINUTES.value:
                    shift_minutes = HistoryTestBase.NUM_CANDLES_FUTURE_CHECK * 30
                self._end_time = (
                    arrow.get(self._start_time)
                    .replace(tzinfo="Asia/Bangkok")
                    .shift(minutes=+shift_minutes)
                    .format("YYYY-MM-DD HH:mm:SS")
                )
            self.__end_time = (
                arrow.get(self._end_time, "YYYY-MM-DD HH:mm:SS").replace(
                    tzinfo="Asia/Bangkok"
                )
                if self._end_time is not None
                else arrow.now().to("Asia/Bangkok")
            )

        return self.__end_time

    def get_kline(self) -> pd.DataFrame:
        if self.__kline is None:
            max_open_time = int(self.get_end_time().timestamp() * 1000)
            min_open_time = int(self.get_start_time().timestamp() * 1000)
            self.__kline = get_candlestick_history_df(
                symbol=UMValue.SYMBOL(),
                start=min_open_time,
                end=max_open_time,
                interval=self._interval,
            )

        return self.__kline.copy()
