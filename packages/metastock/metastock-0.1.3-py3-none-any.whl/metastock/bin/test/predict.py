import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta

from metastock.bin.test.get_history_data import get_history_data
from metastock.modules.com.helper.price_history_df_helper import PriceHistoryDfHelper
from metastock.modules.com.technical_indicator.hullma import Hullma
from metastock.modules.core.logging.logger import Logger

history_data = get_history_data(symbol = 'VCB')

priceHelper = PriceHistoryDfHelper(history_data)

hullma = Hullma(history = history_data)
hulma_data = hullma.get_data()


def predict_trend_change(wma_series, window_size = 5):
    # Khởi tạo DataFrame để lưu kết quả
    result_df = pd.DataFrame(columns = ['Price', 'Predicted_Days_To_Change'])

    # Duyệt qua chuỗi thời gian
    for i in range(len(wma_series) - window_size):
        # Lấy dữ liệu trong cửa sổ hiện tại
        window_data = wma_series.iloc[i:i + window_size]

        # Tính độ dốc (slope) của cửa sổ hiện tại
        X = np.array(range(window_size)).reshape(-1, 1)
        y = window_data.values
        model = LinearRegression()
        model.fit(X, y)
        slope = model.coef_[0]

        # Dự đoán số ngày cần để độ dốc về 0
        if slope != 0:
            days_to_change = -model.intercept_ / slope
        else:
            days_to_change = np.inf  # slope = 0, không đổi

        # Lưu giá và số ngày dự đoán vào DataFrame
        current_day = wma_series.index[i + window_size - 1]
        current_price = wma_series.iloc[i + window_size - 1]
        result_df.loc[current_day] = [current_price, days_to_change]

    return result_df


# Tạo dữ liệu mẫu
dates = pd.date_range('2021-01-01', '2021-01-18')
wma = pd.Series([1, 2, 3, 4, 5, 6, 6.8, 7.2, 7.5, 7.6, 7.5, 6, 5, 4, 3, 2, 1, 0], index = dates)

# Gọi hàm dự đoán
result = predict_trend_change(wma)
print(result)
