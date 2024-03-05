from metastock.modules.core.logging.logger import Logger
from metastock.modules.mbinance.error.invalid_api_response import InvalidApiResponse
from metastock.modules.mbinance.um.api_schema.response.candless_tick import (
    ContinuousContractKline,
    Candlestick,
)
from metastock.modules.mbinance.um.util.get_client import get_um_client
from metastock.modules.mbinance.um.value.um_value import UMValue
from metastock.modules.mbinance.value.common import TimeInterval


def get_klines(
    pair: str,
    start_time: int,
    end_time: int = None,
    time_interval: TimeInterval = TimeInterval.ONE_MINUTE.value,
    contract_type: str = UMValue.CONTRACT_TYPE,
) -> ContinuousContractKline:
    """

    :param pair:
    :param contract_type:
    :param start_time:
    :param end_time:
    :param time_interval:
    """

    logger = Logger()
    um_futures_client = get_um_client()

    logger.debug("Getting klines from {} and to {}".format(start_time, end_time))

    response = um_futures_client.continuous_klines(
        pair=pair,
        contractType=contract_type,
        interval=time_interval,
        startTime=int(start_time),
        endTime=end_time,
        limit=500,
    )
    # logger.debug(f"Klines response {response}")
    try:
        candles_ticks = [
            Candlestick(
                open_time=item[0],
                open=item[1],
                high=item[2],
                low=item[3],
                close=item[4],
                volume=item[5],
                close_time=item[6],
                quote_asset_volume=item[7],
                number_of_trades=item[8],
                taker_buy_volume=item[9],
                taker_buy_quote_asset_volume=item[10],
                ignore=item[11],
            )
            for item in response
        ]
        # candles_ticks.sort(key=lambda item: item.open_time, reverse=True)
        valid_response = ContinuousContractKline(data=candles_ticks)

        logger.debug(f"Success get {len(candles_ticks)} klines from api")
    except Exception as e:
        raise InvalidApiResponse(
            "from get Continuous Contract Kline/Candlestick Data"
        ) from e

    return valid_response
