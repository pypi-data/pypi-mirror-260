import numpy as np
import pandas as pd

from metastock.modules.com.util.avg import avg
from metastock.modules.com.util.price.wma import wma
from metastock.modules.mbinance.um.api_schema.event.kline_event import KlineData


def calc_hull_from_kline(kline: pd.DataFrame) -> pd.Series:
    length = 10
    source = kline.apply(
        lambda row: avg(row["o"], row["c"], row["h"], row["l"]), axis=1
    )
    hulma = wma(
        2 * wma(source, int(length / 2)) - wma(source, length),
        round(np.sqrt(length)),
    )

    return hulma
