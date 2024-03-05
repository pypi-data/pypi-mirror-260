from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.http_client import http_client
from metastock.modules.stockinfo.schema.api_base_response import api_base_response
from metastock.modules.trade.value.url import TradeUrlValue


def get_tick_intraday_speed(symbol: str, date: str):
    logger = Logger()
    url = TradeUrlValue.get_tick_intraday_speed_url(symbol, date)

    # make request to get detail of strategy
    logger.info(f"Will make request call to url [blue]{url}[/blue]")
    response = http_client().get(url)
    strategy_data = response.json()

    api_base_response.validate(strategy_data)

    return strategy_data
