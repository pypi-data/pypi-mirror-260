import pandas as pd


def nearest_peak_index(data: pd.Series):
    diff = data.diff()

    change_sign = (diff * diff.shift(-1)) < 0

    # Lấy index của điểm thay đổi dấu đầu tiên
    peak_or_valley_index = change_sign.idxmax() if change_sign.any() else None

    return peak_or_valley_index
