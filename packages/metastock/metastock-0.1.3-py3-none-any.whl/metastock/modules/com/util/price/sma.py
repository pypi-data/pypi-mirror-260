def sma(series, period):
    """
    Tính Simple Moving Average (SMA) cho một chuỗi dữ liệu.

    :param series: Pandas Series chứa dữ liệu.
    :param period: Số kỳ cho SMA.
    :return: Pandas Series chứa giá trị SMA.
    """
    series = series.iloc[::-1]
    sma = series.rolling(window=period).mean()
    sma = sma.iloc[::-1]

    return sma
