import pandas as pd

from metastock.modules.com.util.avg import avg
from metastock.modules.com.util.price.ema import ema
from metastock.modules.com.util.price.sma import sma
from metastock.modules.mbinance.um.value.um_value import UMValue


def get_wt_status_from_kline(kline: pd.DataFrame):
    n1 = UMValue.WT_N1()
    n2 = UMValue.WT_N2()
    ap = kline.apply(
        lambda row: round(avg(row["close"], row["high"], row["low"]), 4), axis=1
    )
    esa = ema(ap, n1)  # EMA của giá trung bình
    d = ema(abs(ap - esa), n1)  # EMA của độ lệch tuyệt đối giữa giá và EMA
    ci = (ap - esa) / (
        0.015 * d
    )  # Chỉ số kênh hàng hóa (Commodity Channel Index modified)
    tci = ema(ci, n2)  # EMA của CCI

    # Waves Trend Indicator
    wt1 = tci
    wt2 = sma(wt1, 4)
    diff_wt = wt1 - wt2

    return [wt1, wt2, diff_wt]
