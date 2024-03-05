import numpy as np


def linreg(data, length, offset=0):
    x = np.arange(offset, offset + length)  # Tạo mảng index tương ứng với thời gian
    y = data[offset:offset + length]  # Lấy dữ liệu từ offset đến offset + length
    slope, intercept = np.polyfit(x, y, 1)  # Tính toán hệ số dòng hồi quy

    return slope * x + intercept  # Trả về mảng dòng hồi quy
