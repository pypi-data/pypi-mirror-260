from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.app_error import AppError
from metastock.modules.core.util.http_client import http_client
from metastock.modules.trade.value.url import TradeUrlValue


def get_strategy_processes(strategy_hash: str):
    url = TradeUrlValue().get_strategy_processes(strategy_hash=strategy_hash)

    client = http_client()

    Logger().will(f"get strategy processes to url {url}")

    res = client.get(url)

    Logger().info(f"Got response from get strategy {res}")
    if res.status_code != 200:
        raise AppError("Could not get strategy processes data")

    return res.json()
