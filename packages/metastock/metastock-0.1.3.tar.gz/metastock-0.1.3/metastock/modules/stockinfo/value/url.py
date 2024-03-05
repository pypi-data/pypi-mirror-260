import arrow

from metastock.modules.core.util.app_error import AppError
from metastock.modules.core.util.environment import env


class StockInfoUrl:
    TICK_BASE_URL = "https://stock.ngocdiep.top"

    def get_ticker_history_url(
        self,
        symbol: str,
        from_date: str,
        to_date: str = arrow.utcnow().format("YYYY-MM-DD"),
    ):
        base_url = StockInfoUrl.TICK_BASE_URL

        return (
            f"{base_url}/tick/histories?symbol={symbol}&from={from_date}&to={to_date}"
        )

    def get_tick_url(self, symbol: str, date=arrow.utcnow().format("YYYY-MM-DD")):
        base_url = StockInfoUrl.TICK_BASE_URL

        return f"{base_url}/tick/history?symbol={symbol}&date={date}"

    def get_stock_info_url(self, symbol: str):
        base_url = self._get_base_url()

        return f"{base_url}/cor/info?symbol={symbol}"

    def get_price_history_url(self, symbol: str, from_date: str, to_date: str):
        base_url = StockInfoUrl.TICK_BASE_URL

        return f"{base_url}/stock-price/simple-histories?code={symbol}&from={from_date}&to={to_date}"

    def _get_base_url(self):
        if env().get("API_END_POINT") is None:
            raise AppError("Missing PS_API_END_POINT env config")

        return env().get("API_END_POINT")
