def ema(source, period):
    """
    Tính EMA cho một chuỗi giá với kỳ (period) cho trước.

    :param prices: Pandas Series chứa giá.
    :param period: Số kỳ để tính EMA.
    :return: Pandas Series chứa giá trị EMA.
    """
    reversed_source = source.iloc[::-1]
    data = reversed_source.ewm(span=period, adjust=False).mean()
    data = data.iloc[::-1]

    return data
