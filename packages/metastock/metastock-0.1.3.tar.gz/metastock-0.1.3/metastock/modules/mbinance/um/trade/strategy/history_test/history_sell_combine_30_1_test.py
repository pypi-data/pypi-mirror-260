import time

import arrow
import pandas as pd

from metastock.modules.mbinance.um.db.resources.candlestick_resource import (
    get_candlestick_history_df,
)
from metastock.modules.mbinance.um.exchange.connector.api_data_connector import (
    UMApiDataConnector,
)
from metastock.modules.mbinance.um.trade.strategy.config.sell_strategy_v1_config import (
    SellStrategyV1Config,
)
from metastock.modules.mbinance.um.trade.strategy.history_test.history_sell_test import (
    HistorySellTest,
)
from metastock.modules.mbinance.um.trade.strategy.history_test.history_test_base import (
    HistoryTestBase,
)
from metastock.modules.mbinance.um.trade.strategy.sell.msell_v1 import MSellV1Strategy
from metastock.modules.mbinance.um.value.um_value import UMValue
from metastock.modules.mbinance.value.common import TimeInterval


class HistorySellCombine301Test(HistorySellTest):
    def __init__(
        self,
        strategy_config_30m: SellStrategyV1Config,
        strategy_config_1m: SellStrategyV1Config,
        start_time: str,
        end_time: str = None,
    ):
        super().__init__(
            strategy_config=strategy_config_30m,
            interval=TimeInterval.THIRTY_MINUTES,
            start_time=start_time,
            end_time=end_time,
        )
        self._strategy_config_30m = strategy_config_30m
        self._strategy_config_1m = strategy_config_1m

        self.__kline_1m = None
        self.__kline_30m = None

    def get_df(self):
        return self.get_kline_1m()

    def get_kline_1m(self) -> pd.DataFrame:
        if self.__kline_1m is None:
            self.__kline_1m = self.__get_candlestick_history_df(
                interval=TimeInterval.ONE_MINUTE.value,
            )

        return self.__kline_1m.copy()

    def get_kline_30(self) -> pd.DataFrame:
        if self.__kline_30m is None:
            self.__kline_30m = self.__get_candlestick_history_df(
                interval=TimeInterval.THIRTY_MINUTES.value,
            )

        return self.__kline_30m.copy()

    def __get_candlestick_history_df(self, interval: TimeInterval):
        max_open_time = int(self.get_end_time_by_interval(interval).timestamp() * 1000)
        min_open_time = int(
            self.get_start_time_by_interval(interval).timestamp() * 1000
        )
        return get_candlestick_history_df(
            symbol=UMValue.SYMBOL(),
            start=min_open_time,
            end=max_open_time,
            interval=interval,
        )

    def get_start_time_by_interval(self, interval: TimeInterval) -> arrow:
        shift_minutes = UMApiDataConnector.KLINE_HISTORY_SIZE
        if interval == TimeInterval.THIRTY_MINUTES.value:
            shift_minutes = 30 * UMApiDataConnector.KLINE_HISTORY_SIZE
        return (
            arrow.get(self._start_time, "YYYY-MM-DD HH:mm:SS")
            .shift(minutes=-shift_minutes)
            .replace(tzinfo="Asia/Bangkok")
        )

    def get_end_time_by_interval(self, interval: TimeInterval) -> arrow:
        if self._end_time is None:
            shift_minutes = HistoryTestBase.NUM_CANDLES_FUTURE_CHECK
            if interval == TimeInterval.THIRTY_MINUTES.value:
                shift_minutes = HistoryTestBase.NUM_CANDLES_FUTURE_CHECK * 30
            self._end_time = (
                arrow.get(self._start_time)
                .replace(tzinfo="Asia/Bangkok")
                .shift(minutes=+shift_minutes)
                .format("YYYY-MM-DD HH:mm:SS")
            )
        return (
            arrow.get(self._end_time, "YYYY-MM-DD HH:mm:SS").replace(
                tzinfo="Asia/Bangkok"
            )
            if self._end_time is not None
            else arrow.now().to("Asia/Bangkok")
        )

    def start(self):
        df = self.get_kline()
        n_row = df.shape[0] - UMApiDataConnector.KLINE_HISTORY_SIZE
        skip_next_index = None
        start_time = time.time()
        df_30 = self.get_kline_30()
        # Lấy từ phần tử thứ n từ cuối đến phần tử n+120 từ cuối
        for i in range(n_row - 20):
            start_index = n_row - i
            subset = df.iloc[
                start_index - 1 : start_index + UMApiDataConnector.KLINE_HISTORY_SIZE
            ]

            current_candle = subset.iloc[0]
            subset_30 = df_30[
                (df_30.open_time <= current_candle.open_time)
                # & (df_30.close_time >= current_candle.close_time)
            ]
            # check is down trend by hull in 30m timeframe

            if skip_next_index is not None and skip_next_index >= subset.index[0]:
                # self.logger().warning("Skip next index")
                continue

            msell_v1 = MSellV1Strategy(
                kline=subset,
                strategy_config=strategy_config,
            )

            decide = msell_v1.run()
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
