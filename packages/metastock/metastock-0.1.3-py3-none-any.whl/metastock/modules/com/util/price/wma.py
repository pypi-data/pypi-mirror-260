import numpy as np
import pandas as pd


def wma(source: pd.Series, length: int = 20) -> pd.Series:
    """
    Tính Weighted Moving Average (WMA) từ một pandas Series, lùi dần theo thời gian.

    Parameters:
    - source: pd.Series - Series chứa dữ liệu giá
    - length: int - Độ dài của cửa sổ tính toán WMA

    Returns:
    - pd.Series: Series chứa giá trị WMA
    """

    # Tính trọng số
    weights = np.arange(1, length + 1)

    # Đảo ngược Series để tính từ ngày mới nhất đến ngày cũ
    reversed_source = source.iloc[::-1]

    # Áp dụng WMA trên Series đã đảo ngược
    reversed_wma = (
        reversed_source.rolling(window=length)
        .apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
        .round(4)
    )

    # Đảo ngược kết quả để có ngày từ cũ đến mới
    wma_values = reversed_wma.iloc[::-1]

    return wma_values
