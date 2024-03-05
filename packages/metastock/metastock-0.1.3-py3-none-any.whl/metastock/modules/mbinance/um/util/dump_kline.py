import arrow
from pandas import DataFrame

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.environment import is_development


def dump_kline(kline: DataFrame):
    if not is_development():
        return

    new_klines = kline.copy()  # Tạo bản sao của DataFrame gốc

    # Chuyển đổi index của DataFrame mới thành giờ, phút, giây sử dụng Arrow
    new_klines.index = [
        arrow.get(timestamp / 1000).format("HH:mm:ss") for timestamp in new_klines.index
    ]
    Logger().info(new_klines[["is_closed", "number_of_trades", "close"]].head(5))
