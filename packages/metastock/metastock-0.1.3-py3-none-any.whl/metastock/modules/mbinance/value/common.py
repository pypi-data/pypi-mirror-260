from enum import Enum

import arrow


class CommonValue(object):
    API_TESTNET_URL = "https://testnet.binancefuture.com"
    API_TESTNET_STREAM_URL = "wss://stream.binancefuture.com"
    TIME_ZONE = "Asia/Ho_Chi_Minh"

    HISTORICAL_START_TIME = arrow.get("2023-11-01").timestamp() * 1000

    ROUND_DECIMAL = 4


class TimeInterval(Enum):
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"
