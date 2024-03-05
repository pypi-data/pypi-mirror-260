from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.find_common_elements import find_common_elements
from metastock.modules.core.util.http_client import http_client
from metastock.modules.trade.error import StockTradingAnalysisNotFound
from metastock.modules.trade.strategy.filters.filter_abstract import FilterAbstract
from metastock.modules.trade.value.url import TradeUrlValue


class TotalTradeValueFilter(FilterAbstract):
    name = "total_trade_value_filter"

    def __init__(self):
        super().__init__()
        self._analysis_data = None

    def filter(self, symbol: str) -> bool:
        pass

    def get_allowable_list(self) -> list[str]:
        Logger().info("Process total trade value filter")
        client = http_client()

        Logger().info("Will get analysis data from downstream")
        res = client.get(TradeUrlValue().get_stock_trading_analysis_url())

        if res.status_code != 200:
            raise StockTradingAnalysisNotFound()

        self._analysis_data = res.json()

        if not isinstance(self._analysis_data, list) or len(self._analysis_data) == 0:
            raise StockTradingAnalysisNotFound()

        Logger().ok("get analysis data from downstream")

        _input = self.get_input()

        if "total_trade_value_filter" in _input:
            Logger().info(f"Has config for filter total_trade_value_filter: {_input}")

        top = _input["total_trade_value_filter"].get("top") or 50
        if isinstance(_input, dict):
            _input = _input.get("total_trade_value_filter")

            if isinstance(_input, dict) and isinstance(_input.get("top"), int):
                top = _input.get("top")

        Logger().info(f"Total trade value filter config top {top}")

        total_trade_7_days = self._get_top_trade(7, top)
        total_trade_14_days = self._get_top_trade(14, top)
        total_trade_30_days = self._get_top_trade(30, top)

        symbols = find_common_elements(
            total_trade_7_days, total_trade_14_days, total_trade_30_days
        )

        return [symbol for symbol in symbols if len(symbol) == 3]

    def _get_top_trade(self, days: int, top: int):
        sorted_data = sorted(
            self._analysis_data, key=lambda x: x[f"trade_value_{days}"], reverse=True
        )

        return [entry["symbol"] for entry in sorted_data[:top]]
