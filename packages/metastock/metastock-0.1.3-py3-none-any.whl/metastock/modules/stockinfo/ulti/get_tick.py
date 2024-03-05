from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.http_client import http_client
from metastock.modules.stockinfo.value.url import StockInfoUrl


def get_tick(symbol: str, date: str):
    url = StockInfoUrl().get_tick_url(symbol=symbol, date=date)

    Logger().info(f"Will send to API server to get tick  {url}")

    client = http_client()
    res = client.fetch(url=url)

    return res
