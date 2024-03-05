from typing import Optional

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.app_error import AppError
from metastock.modules.core.util.http_client import http_client
from metastock.modules.stockinfo.value.url import StockInfoUrl


def get_tick_history(symbol: str, from_date: str, to_date: Optional[str]):
    url = StockInfoUrl().get_ticker_history_url(
        symbol=symbol, from_date=from_date, to_date=to_date
    )

    client = http_client()

    Logger().info(f"Will send to API server to get tick history {url}")

    res = client.get(url)
    if res.status_code != 200:
        raise AppError("Due to error get tick history data")

    _json = res.json()

    Logger().ok(f"get tick history for {symbol}")
    return sorted(_json, key=lambda x: x["date"], reverse=True)
