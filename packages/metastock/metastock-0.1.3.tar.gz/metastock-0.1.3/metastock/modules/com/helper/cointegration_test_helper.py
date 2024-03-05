# import arrow
# import numpy as np
# import pandas as pd
#
# from metastock.modules.com.misc.engle_granger_cointegration import engle_granger_cointegration
# from metastock.modules.core.logging.logger import Logger
# from metastock.modules.stockinfo.ulti.get_price_history import get_price_history
# from statsmodels.tsa.vector_ar.vecm import coint_johansen, VECM
#
#
# class CointegrationTestHelper:
#
#     def __init__(
#             self, symbol1: str,
#             symbol2: str,
#             from_date: str = arrow.utcnow().shift(months=-6).format('YYYY-MM-DD'),
#             to_date: str = arrow.utcnow().format('YYYY-MM-DD')
#     ):
#         self._cal_price = None
#         self.symbol2 = symbol2
#         self.symbol1 = symbol1
#         self.to_date = to_date
#         self.from_date = from_date
#
#         self.symbol1_prices = None
#         self.symbol2_prices = None
#
#
#     def is_cointegration(self):
#         price_cal = self._calculate_price()
#
#         egc = engle_granger_cointegration(
#                 price_cal['price1'].tolist(), price_cal['price2'].tolist()
#         )
#
#         Logger().info(f'Engle Granger Cointegration between {self.symbol1} and {self.symbol2}: {egc}')
#
#         return egc < 0.05
#
#     def _calculate_price(self):
#         if self._cal_price is None:
#             self.get_prices()
#
#             _prices1 = []
#             _prices2 = []
#
#             for _symbol1_price in self.symbol1_prices[::-1]:
#                 _symbol2_price = next(
#                         (item for item in self.symbol2_prices if item["date"] == _symbol1_price['date']), None
#                 )
#                 if _symbol2_price is not None:
#                     _prices1.append(_symbol1_price['close'])
#                     _prices2.append(_symbol2_price['close'])
#                 else:
#                     Logger().warning(f"Not found price for symbol {self.symbol2} in date: ${_symbol1_price['date']}")
#
#             self._cal_price = {
#                 "price1": np.array(_prices1),
#                 "price2": np.array(_prices2)
#             }
#
#         return self._cal_price
#
#     def beta(self):
#         price_cal = self._calculate_price()
#
#         return np.corrcoef(price_cal['price1'], price_cal['price2'])[0, 1]
#
#     def vecm(self):
#         price_cal = self._calculate_price()
#         data = pd.DataFrame({'A': price_cal['price1'], 'B': price_cal['price2']})
#         # Kiểm tra cointegration bằng coint_johansen
#         result = coint_johansen(data, det_order=0, k_ar_diff=1)
#
#         # Fit VECM model
#         vecm = VECM(data, coint_rank=1)
#         vecm_fitted = vecm.fit()
#
#         # Hệ số trong mô hình VECM
#         alpha = vecm_fitted.alpha  # speed of adjustment
#         beta = vecm_fitted.beta  # cointegration relationship
#
#         return {
#             "cointegration": result,
#             "vecm_alpha"   : alpha,
#             "vecm_beta"    : beta
#         }
#
#     def get_prices(self):
#         if self.symbol1_prices is None:
#             self.symbol1_prices = get_price_history(self.symbol1, self.from_date, self.to_date)
#
#         if self.symbol2_prices is None:
#             self.symbol2_prices = get_price_history(self.symbol2, self.from_date, self.to_date)
