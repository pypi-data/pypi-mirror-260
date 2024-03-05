import arrow

from metastock.modules.mbinance.um.exchange.general.time.get_server_time import (
    get_server_time_ms,
)


def get_last_minutes(minutes: int = 1):
    server_time_ms = get_server_time_ms()

    return int(
        arrow.get(server_time_ms / 1000).shift(minutes=-minutes).timestamp() * 1000
    )
