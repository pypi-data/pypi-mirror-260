import math

import numpy as np
import pandas as pd


def predict_trend_change(wma_series: pd.Series, n: int) -> pd.DataFrame:
    results = []

    for i in range(n, len(wma_series)):
        y = wma_series.iloc[i - n:i][::-1].diff().values[1:]  # Bỏ qua giá trị đầu tiên NaN từ .diff()
        x = np.arange(len(y))

        # Áp dụng bình phương nhỏ nhất để tìm hệ số góc
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]

        # Dự đoán số ngày để đổi chiều
        if m != 0:
            days_to_zero = -c / m
        else:
            days_to_zero = np.inf  # Nếu m = 0, không thể dự đoán khi nào đổi chiều
            trend = "Stable"

        results.append(
            {
                "date": wma_series.index[i - n],
                "slope": m,
                "estimate_day_change": days_to_zero if 0 < days_to_zero < 3 else None
            }
        )

    return pd.DataFrame(results).set_index("date")


def predict_trend_change_v1(series: pd.Series, n: int = 3) -> pd.DataFrame:
    results = []
    diff = series[::-1].diff()

    for i in range(n, len(series)):
        y = diff.iloc[i - n + 1:i + 1]

        last = {
            "date": diff.index[i],
            "estimate_day_change": None,
            "next_day": False
        }

        if not math.isnan(diff.iloc[i]) and diff.iloc[i] != 0:
            if diff.iloc[i] * diff.iloc[i - 1] < 0:
                # doi dau chung to vua di qua 0
                last = {
                    "date": diff.index[i],
                    "estimate_day_change": 0,
                    "next_day": False,
                    "trend": 'down' if diff.iloc[i - 1] > 0 else 'up'
                }
            else:
                z = y[::-1].diff()
                mean_abs = z.abs().mean()

                if not math.isnan(mean_abs) and mean_abs > 0:
                    day_change = abs(diff.iloc[i] / mean_abs)
                    last = {
                        "date": diff.index[i],
                        "estimate_day_change": day_change,
                        "next_day": True if not math.isnan(day_change)
                                            and (
                                                    day_change < 1
                                                    or (last['estimate_day_change'] is not None and
                                                        last['estimate_day_change'] / day_change > 2 and
                                                        day_change < 5))
                                            and (last is None or last['estimate_day_change'] != 0) else False,
                        "trend": 'down' if diff.iloc[i] > 0 else 'up'
                    }

        results.append(
            last
        )

    return pd.DataFrame(results).set_index("date")
