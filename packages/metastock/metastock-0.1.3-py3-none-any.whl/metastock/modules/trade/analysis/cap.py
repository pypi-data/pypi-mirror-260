from metastock.modules.stockinfo.ulti.get_symbol_info import get_symbol_info
from metastock.modules.trade.analysis.abstract_analysis import AbstractStockTradingAnalysis
import numbers


class StockTradingAnalysisCap(AbstractStockTradingAnalysis):
    def get_data(self):
        prices = self.get_price_history()

        if len(prices) == 0:
            return {}

        latest_price = prices[0]

        symbol_info = get_symbol_info(self.get_symbol())

        if (symbol_info is None
                or not isinstance(latest_price['close'], numbers.Number)
                or not isinstance(symbol_info['totalShares'], numbers.Number)):
            return {}

        return {
            "cap": round(latest_price['close'] * symbol_info['totalShares'] / 10 ** 9)
        }
