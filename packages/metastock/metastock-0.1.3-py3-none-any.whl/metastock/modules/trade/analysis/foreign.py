from metastock.modules.com.helper.price_history_df_helper import PriceHistoryDfHelper
from metastock.modules.core.logging.logger import Logger
from metastock.modules.stockinfo.ulti.get_price_history import get_price_history


class StockTradingAnalysisForeign:
    def __init__(self, symbol: str, price_history: list = None):
        self._price_helper = None
        self._price_history = price_history
        self._symbol = symbol

    def get_data(self):
        info_30_days = self._build_data_for_days(days=30)
        info_15_days = self._build_data_for_days(days=15)
        info_7_days = self._build_data_for_days(days=7)

        return {**info_30_days, **info_15_days, **info_7_days}

    def _build_data_for_days(self, days: int):
        data = {}
        info_days = self.get_info_days(days=days)
        if info_days:
            data[f"foreign_buy_{days}"] = info_days["buy"]
            data[f"foreign_sell_{days}"] = info_days["sell"]
            data[f"foreign_diff_{days}"] = info_days["diff"]

        return data

    def get_info_days(self, days: int):
        price_helper = self._get_price_history_helper()
        price_df = price_helper.get_df()
        top_n = price_df.head(days)

        if len(top_n) != days:
            Logger().error("Not enough days left to calculate foreign")
            return None

        sum_buy = round(top_n["fBuyVal"].sum() / 10**3)
        sum_sell = round(top_n["fSellVal"].sum() / 10**3)
        diff = sum_buy - sum_sell

        return {"buy": sum_buy, "sell": sum_sell, "diff": diff}

    def _get_price_history_helper(self) -> PriceHistoryDfHelper:
        if self._price_helper is None:
            self._price_helper = PriceHistoryDfHelper(self.get_price_history())

        return self._price_helper

    def get_symbol(self):
        return self._symbol

    def get_price_history(self):
        if self._price_history is None:
            self._price_history = get_price_history(symbol=self.get_symbol())

        return self._price_history
