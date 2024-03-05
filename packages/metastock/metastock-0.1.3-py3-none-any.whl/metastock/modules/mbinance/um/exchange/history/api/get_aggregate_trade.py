from metastock.modules.core.logging.logger import Logger
from metastock.modules.mbinance.error.invalid_api_response import InvalidApiResponse
from metastock.modules.mbinance.um.api_schema.response.aggregate_trade_list import (
    AggregateTradeList,
)
from metastock.modules.mbinance.um.util.get_client import get_um_client
from metastock.modules.mbinance.um.value.um_value import UMValue


def get_aggregate_trade(
    symbol: str, start_time: int, end_time: int = None
) -> AggregateTradeList:
    logger = Logger()
    um_futures_client = get_um_client()

    logger.info("Getting Compressed/Aggregate Trades List")

    if end_time - start_time > 60 * 10**6:
        end_time = start_time + 60 * 10**6 - 1000

    response = um_futures_client.agg_trades(
        symbol=symbol, startTime=start_time, endTime=end_time, limit=1000
    )

    try:
        # aggregate_trade_data = [BinanceTradeData(**item) for item in response]
        valid_response = AggregateTradeList(data=response)
    except Exception as e:
        raise InvalidApiResponse("from get Compressed/Aggregate Trades List") from e

    logger.ok("get Compressed/Aggregate Trades")
    return valid_response
