import math

import numpy as np
import pandas as pd

from metastock.modules.com.util.avg import avg
from metastock.modules.com.util.nearest_peak_index import nearest_peak_index
from metastock.modules.com.util.price.wma import wma
from metastock.modules.core.util.registry import registry
from metastock.modules.mbinance.um.value.um_value import UMValue


def get_hull_from_kline(kline: pd.DataFrame) -> pd.Series:
    length = UMValue.HULL_LENGTH()
    source = kline.apply(
        lambda row: avg(row["open"], row["close"], row["high"], row["low"]), axis=1
    )

    hulma = wma(
        2 * wma(source, int(length / 2)) - wma(source, length),
        round(np.sqrt(length)),
    )

    return hulma


def get_hull_status(hull: pd.Series):
    hull_ca_revert = hull[::-1].diff()
    hull_ca = hull_ca_revert[::-1]
    nearest_index = nearest_peak_index(hull_ca)

    # xem trend hiện tại và tìm hệ số góc hiện tại
    if nearest_index is None:
        return None

    period_range = abs(hull_ca.index.get_loc(nearest_index))
    if hull_ca.loc[nearest_index] > hull_ca.iloc[0]:
        trend = -1
        slope = math.atan(
            (period_range * 10) / abs(hull_ca.loc[nearest_index] - hull_ca.iloc[0])
        )
    else:
        trend = 1
        slope = math.atan(
            abs(hull_ca.loc[nearest_index] - hull_ca.iloc[0]) / (period_range * 10)
        )

    slope = math.degrees(slope)

    # trend, slope, range, đỉnh/đáy, giá trị hiện tại
    return trend, slope, period_range, hull_ca.loc[nearest_index], hull_ca.iloc[0]
