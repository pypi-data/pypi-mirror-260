from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.http_client import http_client
from metastock.modules.stockinfo.ulti.error import CouldNotGetSymbolInfo
from metastock.modules.stockinfo.value.url import StockInfoUrl


def get_symbol_info(symbol: str):
    url = StockInfoUrl().get_stock_info_url(symbol=symbol)

    client = http_client()

    Logger().info(f"Will send to API server to get symbol info {url}")

    res = client.get(url)
    if res.status_code != 200:
        raise CouldNotGetSymbolInfo("Due to error get price history data")

    _json = res.json()

    Logger().ok(f"get symbol info for {symbol}")

    return _json
