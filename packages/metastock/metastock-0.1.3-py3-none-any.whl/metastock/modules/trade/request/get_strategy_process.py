from jsonschema import validate

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.http_client import http_client
from metastock.modules.trade.request.schema.response import GET_STRATEGY_PROCESS_SCHEMA
from metastock.modules.trade.value.url import TradeUrlValue


def get_strategy_process(hash_key: str, symbol: str) -> dict:
    """

    :rtype: dict
    """
    # try:
    logger = Logger()
    url = (
        f"{TradeUrlValue.TRADING_STRATEGY_PROCESS_URL}?hash={hash_key}&symbol={symbol}"
    )

    # make request to get detail of strategy
    logger.info(f"Will make request call to url [blue]{url}[/blue]")
    response = http_client().get(url)
    strategy_data = response.json()

    validate(strategy_data, GET_STRATEGY_PROCESS_SCHEMA)

    return strategy_data


# except Exception as e:
