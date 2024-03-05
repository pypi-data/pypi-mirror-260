import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf

from metastock.modules.core.util.get_json_data import get_json_data

def linreg(data, length, offset):
    x = np.arange(offset, offset + length)  # Tạo mảng index tương ứng với thời gian
    y = data[offset:offset + length]  # Lấy dữ liệu từ offset đến offset + length
    slope, intercept = np.polyfit(x, y, 1)  # Tính toán hệ số dòng hồi quy

    return slope * x + intercept  # Trả về mảng dòng hồi quy

# Tạo dữ liệu giả định từ API hoặc tệp JSON
data = get_json_data("http://localhost:3000/stock-price/history?code=BFC&from=2022-07-01")
df = pd.DataFrame(data)
close_prices = df["close"].tolist()

length = 100
offset = 0
linear_regression = linreg(close_prices, length, offset)

# Chuyển định dạng cột "date" thành datetime
df["date"] = pd.to_datetime(df["date"])

# Đặt cột "date" làm chỉ số
df.set_index("date", inplace=True)

# Vẽ biểu đồ nến và đường dòng hồi quy
plt.figure(figsize=(12, 6))

# Biểu đồ nến
ax1 = plt.subplot(2, 1, 1)
mpf.plot(df, type='candle', style='charles', ax=ax1)
plt.title('Candlestick Chart')

# Biểu đồ đường dòng hồi quy
# ax2 = plt.subplot(2, 1, 2, sharex=ax1)
# ax2.plot(df.index[offset:offset+length], linear_regression, linestyle='--', color='r', label='Linear Regression')
# ax2.set_xlabel('Date')
# ax2.set_ylabel('Price')
# ax2.legend()
# plt.title('Linear Regression')
#
plt.tight_layout()
plt.show()