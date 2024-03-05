from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.app_error import AppError
from metastock.modules.core.util.http_client import http_client
from metastock.modules.trade.value.url import TradeUrlValue


def get_strategy_process_actions(strategy_hash, symbol: str):
    url = TradeUrlValue().get_strategy_process_actions(
        strategy_hash=strategy_hash, symbol=symbol
    )

    client = http_client()

    Logger().will(f"get strategy process actions to url {url}")

    res = client.get(url)

    Logger().info(f"Got response from get strategy process actions {res}")
    if res.status_code != 200:
        raise AppError("Could not get strategy process actions data")

    return res.json()
