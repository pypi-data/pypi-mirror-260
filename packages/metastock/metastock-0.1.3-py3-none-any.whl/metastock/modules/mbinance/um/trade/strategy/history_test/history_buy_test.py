import arrow
from rich.panel import Panel
from rich.table import Table

from metastock.modules.mbinance.um.exchange.connector.api_data_connector import (
    UMApiDataConnector,
)
from metastock.modules.mbinance.um.trade.strategy.buy.mbuy_v1 import MBuyV1Strategy
from metastock.modules.mbinance.um.trade.strategy.history_test.history_test_base import (
    HistoryTestBase,
)
from metastock.modules.mbinance.um.value.trade_strategy_type import DecideInfo
from metastock.modules.mbinance.um.value.um_buy_strategy_value import UMBuyStrategyValue


class HistoryBuyTest(HistoryTestBase):
    def __check_can_tp_or_cl(self, buy_price: float, index):
        df = self.get_kline()
        df_future = df.loc[df.index > index].copy()
        df_future.sort_index(ascending=True, inplace=True)

        tps = df_future[
            df_future["high"]
            >= round(buy_price * (100 + UMBuyStrategyValue.TP_PRICE_PERCENT) / 100, 4)
        ]
        first_tp_index = tps.index[0] if len(tps) > 0 else None
        cls = df_future[
            df_future["low"]
            <= round(buy_price * (100 - UMBuyStrategyValue.CL_PRICE_PERCENT) / 100, 4)
        ]
        first_cl_index = cls.index[0] if len(cls) > 0 else None

        can_tp = False
        if first_tp_index is not None:
            if first_cl_index is not None:
                can_tp = first_tp_index <= first_cl_index
            if first_cl_index is None:
                can_tp = True

        return [can_tp, first_tp_index, first_cl_index]

    def start(self):
        count = {"pass": 0, "fail": 0, "unknown": 0}
        summary_data = []
        df = self.get_kline()
        n_row = df.shape[0] - UMApiDataConnector.KLINE_HISTORY_SIZE

        # Lấy từ phần tử thứ n từ cuối đến phần tử n+120 từ cuối
        for i in range(len(df) - UMApiDataConnector.KLINE_HISTORY_SIZE - 20):
            # TODO: check skipp if i nam trong rang cua TP hoac CL truoc do

            start_index = n_row - i
            subset = df.iloc[
                start_index - 1 : start_index + UMApiDataConnector.KLINE_HISTORY_SIZE
            ]
            # self.logger().info(f"Check for {subset.index[0]}")
            mbuy_v1 = MBuyV1Strategy(kline=subset)

            # start_time = time.time()
            decide = mbuy_v1.run()  # end_time = time.time()
            # execution_time = end_time - start_time
            # self.logger().info(f"{decide.message}")
            if isinstance(decide, DecideInfo) and decide.open_pos:
                self.logger().info(
                    f"=>>> {subset.index[0]} Chờ để mở vị thế mua tại giá  ({decide.min_open_pos} -> {decide.max_open_pos})"
                )
                low_price = subset.iloc[0]["low"]
                high_price = subset.iloc[0]["high"]

                open_buy_pos_price = None

                if decide.min_open_pos <= low_price:
                    self.logger().info(
                        f"Mở mua ngay tại giá OPEN {subset.iloc[0]['open']}"
                    )
                    open_buy_pos_price = subset.iloc[0]["open"]
                elif high_price >= decide.min_open_pos:
                    self.logger().info(f"Mở mua tại giá MIN {decide.min_open_pos}")
                    open_buy_pos_price = decide.min_open_pos
                else:
                    self.logger().info("Không thể mở vị thế vì không có giá phù hợp")
                    summary_data.append(
                        {
                            "time": subset.index[0],
                            "status": "[white]None",
                            "price": f"{decide.min_open_pos} -> {decide.max_open_pos}",
                            "tp": None,
                            "cl": None,
                        }
                    )
                    count["unknown"] = count["unknown"] + 1

                if open_buy_pos_price is not None:
                    # Check if can TP or must CL
                    check_tp_or_cl = self.__check_can_tp_or_cl(
                        buy_price=open_buy_pos_price, index=subset.index[0]
                    )
                    if not check_tp_or_cl[0]:
                        self.logger().console().print(
                            Panel(
                                f"{subset.index[0]} [b yellow]{open_buy_pos_price}[/b yellow], Cut Loss at {check_tp_or_cl[2]}",
                                title="[red]FAILED",
                                # subtitle="Thank you",
                            )
                        )
                        count["fail"] = count["fail"] + 1
                        summary_data.append(
                            {
                                "time": subset.index[0],
                                "status": "[red]Failed",
                                "price": open_buy_pos_price,
                                "tp": None,
                                "cl": check_tp_or_cl[2],
                            }
                        )
                    else:
                        self.logger().cionsole().print(
                            Panel(
                                f"{subset.index[0]} [b yellow]{open_buy_pos_price}[/b yellow], Take Profit at {check_tp_or_cl[1]}, CL tại {check_tp_or_cl[2]}",
                                title="[green]PASS",
                                # subtitle="Thank you",
                            )
                        )
                        count["pass"] = count["pass"] + 1
                        summary_data.append(
                            {
                                "time": subset.index[0],
                                "status": "[green]Pass",
                                "price": open_buy_pos_price,
                                "tp": check_tp_or_cl[1],
                                "cl": check_tp_or_cl[2],
                            }
                        )

        table = Table(
            title=f"Pass [green b]{count['pass']}[/green b] / Fail [red b]{count['fail']}[/red b] / Unknown [yellow b]{count['unknown']}[/yellow b]"
        )
        table.add_column("Time", justify="right", style="cyan", no_wrap=True)
        table.add_column("Status", style="magenta")
        table.add_column("Price", justify="right", style="green")
        table.add_column("TP", justify="right", style="green")
        table.add_column("CL", justify="right", style="green")

        for row in summary_data:
            table.add_row(
                arrow.get(row["time"]).format("HH:mm YYYY-MM-DD"),
                row["status"],
                str(row["price"]),
                arrow.get(row["tp"]).format("HH:mm YYYY-MM-DD")
                if row["tp"] is not None
                else "",
                arrow.get(row["cl"]).format("HH:mm YYYY-MM-DD")
                if row["cl"] is not None
                else "",
            )

        self.logger().console().print(table, justify="center")
