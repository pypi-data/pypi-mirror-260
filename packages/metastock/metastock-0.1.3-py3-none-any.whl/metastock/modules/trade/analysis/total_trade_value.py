from metastock.modules.com.helper.price_history_df_helper import PriceHistoryDfHelper
from metastock.modules.core.logging.logger import Logger


class StockTradingAnalysisTotalTradeValue:
    def __init__(self, symbol: str, price_history: list):
        self._price_history = price_history
        self._price_helper = None
        self._symbol = symbol

    def get_data(self):
        trade_value_7 = self._calculate_trade_value(7)
        trade_value_14 = self._calculate_trade_value(14)
        trade_value_30 = self._calculate_trade_value(30)

        return {
            "trade_value_7": trade_value_7,
            "trade_value_14": trade_value_14,
            "trade_value_30": trade_value_30,
        }

    def _calculate_trade_value(self, day_before: int):
        Logger().info(
            f"Will calculate trade value for '{self.get_symbol()}' in {day_before} days"
        )
        df = (
            self._get_price_history_helper(price_history=self._price_history)
            .get_df()
            .head(day_before)
        )

        return round(df["value"].sum() / (day_before * 10**3), 0)

    def _get_price_history_helper(self, price_history) -> PriceHistoryDfHelper:
        if self._price_helper is None:
            self._price_helper = PriceHistoryDfHelper(price_history)

        return self._price_helper

    def get_symbol(self):
        return self._symbol
