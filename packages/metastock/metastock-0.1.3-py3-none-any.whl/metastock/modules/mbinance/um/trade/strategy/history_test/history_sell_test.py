import time

import arrow
from pandas import DataFrame
from rich.panel import Panel

from metastock.modules.mbinance.um.exchange.connector.api_data_connector import (
    UMApiDataConnector,
)
from metastock.modules.mbinance.um.trade.strategy.history_test.history_test_base import (
    HistoryTestBase,
)
from metastock.modules.mbinance.um.trade.strategy.sell.msell_v1 import MSellV1Strategy
from metastock.modules.mbinance.um.value.trade_strategy_type import DecideInfo


class HistorySellTest(HistoryTestBase):
    def _check_can_tp_or_cl(self, buy_price: float, index):
        df = self.get_kline()
        df_future = df.loc[df.index >= index].copy()
        df_future.sort_index(ascending=True, inplace=True)

        tps = df_future[
            df_future["low"]
            <= round(buy_price * (100 - self._strategy_config.get_tp()) / 100, 4)
        ]
        first_tp_index = tps.index[0] if len(tps) > 0 else None
        cls = df_future[
            df_future["high"]
            >= round(buy_price * (100 + self._strategy_config.get_sl()) / 100, 4)
        ]
        first_cl_index = cls.index[0] if len(cls) > 0 else None

        can_tp = False
        max_tp_price = None  # Khi bị stop loss thì giá cao nhất có thể TP là bao nhiêu (cho cả 2 trường hợp có thể TP hoặc không)

        if first_cl_index is not None:
            in_sl_df = df_future.loc[df_future.index <= first_cl_index]
            max_tp_price = in_sl_df["low"].min()
            max_tp_price = (
                f"{max_tp_price}({round((buy_price-max_tp_price)*100/buy_price,2)}%)"
            )

        max_sl_price = None
        if first_tp_index is not None:
            in_tp_df = df_future.loc[df_future.index <= first_tp_index]
            max_sl_price = in_tp_df["high"].max()
            max_sl_price = (
                f"{max_sl_price}({round((max_sl_price-buy_price)*100/buy_price,2)}%)"
            )
            if first_cl_index is not None:
                # Chỗ này đang ưu tiên CUT LOSS ĐỂ CÓ THỂ AN TOÀN
                can_tp = first_tp_index <= first_cl_index
            if first_cl_index is None:
                can_tp = True

        return [can_tp, first_tp_index, first_cl_index, max_tp_price, max_sl_price]

    def process_decide(self, subset: DataFrame, decide: DecideInfo):
        skip_next_index = None
        if isinstance(decide, DecideInfo) and decide.open_pos:
            self.logger().info(
                f"Chờ để mở vị thế BÁN tại giá  ({decide.min_open_pos} -> {decide.max_open_pos})"
            )
            low_price = subset.iloc[0]["low"]
            high_price = subset.iloc[0]["high"]
            open_price = subset.iloc[0]["open"]

            open_buy_pos_price = None

            price_position = ""
            if low_price <= decide.min_open_pos <= high_price:
                self.logger().info(
                    f"Mở mua tại giá MIN __(ĐẸP NHẤT)__ {decide.min_open_pos}"
                )
                open_buy_pos_price = decide.min_open_pos
                price_position = "MIN"
            elif decide.max_open_pos <= high_price <= decide.min_open_pos:
                if open_price >= decide.max_open_pos:
                    self.logger().info(
                        f"Mở mua tại giá OPEN __(ĐÃ QUA ĐIỂM MUA ĐẸP NHẤT)__ {open_price}"
                    )
                    open_buy_pos_price = open_price
                    price_position = "OPEN"
                else:
                    self.logger().info(
                        f"Mở mua tại giá CUT LOSS __(RẤT RỦI RO)__ {decide.max_open_pos}"
                    )
                    open_buy_pos_price = decide.max_open_pos
                    price_position = "CL"
            elif decide.min_open_pos >= high_price >= decide.max_open_pos >= low_price:
                self.logger().info(
                    f"Mở mua tại giá CUT LOSS __(RẤT RỦI RO)__ {decide.max_open_pos}"
                )
                open_buy_pos_price = decide.max_open_pos
                price_position = "CL"
            else:
                self.logger().info("Không thể mở vị thế vì không có giá phù hợp")
                self._add_to_results(
                    dt=subset.index[0],
                    status="UNKNOWN",
                    price=None,
                    price_min=decide.min_open_pos,
                    price_max=decide.max_open_pos,
                    price_position=None,
                    tp=None,
                    cl=None,
                )

            if open_buy_pos_price is not None:
                # Check if can TP or must CL
                check_tp_or_cl = self._check_can_tp_or_cl(
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
                    self._add_to_results(
                        dt=subset.index[0],
                        status="FAIL",
                        price=open_buy_pos_price,
                        price_min=decide.min_open_pos,
                        price_max=decide.max_open_pos,
                        price_position=price_position,
                        tp=None,
                        cl=check_tp_or_cl[2],
                        max_tp_price=check_tp_or_cl[3],
                        # max_sl_price=check_tp_or_cl[4],
                    )
                    skip_next_index = check_tp_or_cl[2]
                else:
                    self.logger().console().print(
                        Panel(
                            f"{subset.index[0]} [b yellow]{open_buy_pos_price}[/b yellow], Take Profit at {check_tp_or_cl[1]}, CL tại {check_tp_or_cl[2]}",
                            title="[green]PASS",
                            # subtitle="Thank you",
                        )
                    )
                    self._add_to_results(
                        dt=subset.index[0],
                        status="PASS",
                        price=open_buy_pos_price,
                        price_min=decide.min_open_pos,
                        price_max=decide.max_open_pos,
                        price_position=price_position,
                        tp=check_tp_or_cl[1],
                        cl=check_tp_or_cl[2],
                        max_tp_price=check_tp_or_cl[3],
                        max_sl_price=check_tp_or_cl[4],
                    )
                    skip_next_index = check_tp_or_cl[1]

        return skip_next_index

    def start(self):
        df = self.get_kline()
        n_row = df.shape[0] - UMApiDataConnector.KLINE_HISTORY_SIZE
        skip_next_index = None
        start_time = time.time()
        # Lấy từ phần tử thứ n từ cuối đến phần tử n+120 từ cuối
        for i in range(n_row - HistoryTestBase.NUM_CANDLES_FUTURE_CHECK):
            start_index = n_row - i
            subset = df.iloc[
                start_index - 1 : start_index + UMApiDataConnector.KLINE_HISTORY_SIZE
            ]
            if skip_next_index is not None and skip_next_index >= subset.index[0]:
                # self.logger().warning("Skip next index")
                continue
            self.logger().info(
                f"{arrow.get(subset.index[0]).format('HH:mm YYYY-MM-DD')} Analyzing..."
            )
            msell_v1 = MSellV1Strategy(
                kline=subset, strategy_config=self._strategy_config
            )

            try:
                decide = msell_v1.run()
            except Exception as e:
                self.logger().exception(e, exc_info=True)
                continue

            self.logger().info(
                f"{arrow.get(subset.index[0]).format('HH:mm YYYY-MM-DD')} --------------------{decide.message}--------------------{decide.code}"
            )
            skip_next_index = self.process_decide(subset, decide)

        end_time = time.time()
        execution_time = end_time - start_time
        self.logger().info(
            f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Exceed execute time {execution_time}"
        )
        self._write_to_cli()
        self.write_results_to_excel()
