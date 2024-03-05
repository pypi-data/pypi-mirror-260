import arrow
from pydantic import ValidationError

from metastock.modules.mbinance.error.invalid_api_response import InvalidApiResponse
from metastock.modules.mbinance.um.api_schema.response.server_time import ServerTime
from metastock.modules.mbinance.um.util.get_client import get_um_client
from metastock.modules.mbinance.value.common import CommonValue


def get_server_time_ms() -> int:
    um_futures_client = get_um_client()
    server_time = um_futures_client.time()

    try:
        server_time = ServerTime(**server_time)

        return server_time.serverTime
    except ValidationError as e:
        raise InvalidApiResponse(message="Invalid server time") from e


def get_server_time(human: bool = False, timezone: bool = False) -> int | str:
    server_time_ms = get_server_time_ms()

    if human:
        timestamp = server_time_ms / 1000
        arrow_time_utc = arrow.get(timestamp)

        if timezone:
            arrow_tz = arrow_time_utc.to(CommonValue.TIME_ZONE)

            return arrow_tz.format("YYYY-MM-DD HH:mm:ss ZZ")

        return arrow_time_utc.format("YYYY-MM-DD HH:mm:ss ZZ")

    return server_time_ms
