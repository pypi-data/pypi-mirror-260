from enum import Enum


class UMEventType(Enum):
    CONTINUOUS_KLINE = "continuous_kline"
    ORDER_TRADE_UPDATE = "ORDER_TRADE_UPDATE"
    ACCOUNT_UPDATE = "ACCOUNT_UPDATE"
