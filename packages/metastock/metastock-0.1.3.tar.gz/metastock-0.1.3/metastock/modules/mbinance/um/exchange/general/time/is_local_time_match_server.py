import arrow

from metastock.modules.core.logging.logger import Logger
from metastock.modules.mbinance.um.exchange.general.time.get_server_time import (
    get_server_time,
)


def is_local_time_match_server(diff_max=2) -> bool:
    logger = Logger()

    server_time = arrow.get(get_server_time() / 1000)
    local_time = arrow.now()

    time_diff = abs(local_time - server_time).total_seconds()
    logger.info(f"Time difference between local and server: {time_diff} seconds")

    return time_diff <= diff_max
