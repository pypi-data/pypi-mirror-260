import arrow

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.http_client import http_client
from metastock.modules.stockinfo.ulti.error import CouldNotGetPriceHistory
from metastock.modules.stockinfo.value.url import StockInfoUrl


def get_price_history(
    symbol: str,
    from_date: str = None,
    to_date: str = arrow.utcnow().format("YYYY-MM-DD"),
    raise_empty_exception=True,
):
    if from_date is None:
        current_date = arrow.now()
        from_date = current_date.shift(months=-6).format("YYYY-MM-DD")

    url = StockInfoUrl().get_price_history_url(
        symbol=symbol, from_date=from_date, to_date=to_date
    )

    client = http_client()

    Logger().info(f"Will send to API server to get history price {url}")

    res = client.get(url)
    if res.status_code != 200:
        raise CouldNotGetPriceHistory("Due to error get price history data")

    _json = res.json()
    data = _json["data"]

    if raise_empty_exception is True and (not isinstance(data, list) or len(data)) == 0:
        raise CouldNotGetPriceHistory(f"Due to price history is EMPTY {symbol}")

    Logger().ok(f"get price history for {symbol}")
    return sorted(data, key=lambda x: x["date"], reverse=True)
