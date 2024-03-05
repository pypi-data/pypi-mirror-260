# import pandas as pd
# import numpy as np
# from statsmodels.tsa.stattools import coint
#
#
# def engle_granger_cointegration(symbol1_prices: list, symbol2_prices: list):
#     price_A = np.array([1, 2, 3, 4, 5, 6])  # Thay thế bằng dữ liệu thực
#     price_B = np.array([2, 3, 4, 3, 2, 1])  # Thay thế bằng dữ liệu thực
#
#     # Thực hiện Engle-Granger cointegration test
#     score, p_value, _ = coint(price_A, price_B)
#
#     return p_value
