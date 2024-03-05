import numpy as np
import pandas as pd

from metastock.modules.com.technical_indicator.technical_indicator_abstract import TechnicalIndicatorAbstract
from metastock.modules.com.util.avg import avg
from metastock.modules.com.util.linreg import linreg
from metastock.modules.com.util.price_history_helper import PriceHistoryHelper


class SqzMomConfig:
    length_bb: int
    mult_bb: int
    length_kc: int
    mult_kc: float

    def __init__(
            self, length_bb = 20, mult_bb = 2, length_kc = 20, mult_kc = 1.5, use_true_range = True,
            cal_source_func = lambda row: row['close']
    ):
        self.use_true_range = use_true_range
        self.cal_source_func = cal_source_func
        self.mult_kc = mult_kc
        self.length_kc = length_kc
        self.mult_bb = mult_bb
        self.length_bb = length_bb


class SqzMom(TechnicalIndicatorAbstract):
    def set_config(self, config: SqzMomConfig):
        return super().set_config(config)

    # def get_data(self):
    #     super().get_data()
    #     config: SqzMomConfig = self.get_config()
    #     price_helper: PriceHistoryHelper = self.get_price_history_helper()
    #
    #     # Define date
    #     self.get_price_history_helper().set_date(self.get_date())
    #
    #     source_func = config.cal_source_func
    #
    #     # Calculate BB
    #     basic = price_helper.sma_by_source_func(config.length_bb, source_func)
    #     dev = config.mult_bb * price_helper.stdev(config.length_bb, source_func)
    #     upperBB = round(basic + dev)
    #     lowerBB = round(basic - dev)
    #
    #     # Calculate KC
    #     ma = price_helper.sma_by_source_func(config.length_kc, source_func)
    #     range_ma = self._get_range_sma(self.get_date())
    #     upperKC = round(ma + range_ma * config.mult_kc)
    #     lowerKC = round(ma - range_ma * config.mult_kc)
    #
    #     sqzOn = (lowerBB > lowerKC) and (upperBB < upperKC)
    #     sqzOff = (lowerBB < lowerKC) and (upperBB > upperKC)
    #     noSqz = (sqzOn == False) and (sqzOff == False)
    #
    #     value = round(self._get_value()[0])
    #
    #     return value, sqzOn, sqzOff, noSqz
    #
    # def _get_value(self):
    #     config: SqzMomConfig = self.get_config()
    #     helper: PriceHistoryHelper = self.get_price_history_helper()
    #     length = config.length_kc
    #     values = []
    #
    #     date = self.get_date()
    #     for i in range(length):
    #         # Set the target date for calculating true range
    #         helper.set_date(date)
    #         source = helper.get_row_data_by_source_func(config.cal_source_func)
    #
    #         sma = helper.sma(length)
    #         subset_rows: pd.DataFrame = helper.get_subset_rows_by_date(date, length)
    #
    #         if not isinstance(subset_rows, pd.DataFrame):
    #             return None
    #
    #         highest_high = subset_rows['high'].max()
    #         lowest_low = subset_rows['low'].min()
    #
    #         values.append(source - avg(avg(highest_high, lowest_low), sma))
    #
    #         # Move to the previous date
    #         date = helper.get_previous_row_by_date(date)['date']
    #
    #     return linreg(values, length)
    #
    # def _get_range_sma(self, date: str) -> float | None:
    #     config: SqzMomConfig = self.get_config()
    #     helper: PriceHistoryHelper = self.get_price_history_helper()
    #     length = config.length_kc
    #     # Create an empty list to store the true range values
    #     true_range_values = []
    #
    #     # Iterate over the specified length
    #     for i in range(length):
    #         # Set the target date for calculating true range
    #         helper.set_date(date)
    #
    #         true_range = None
    #         if config.use_true_range:
    #             # Calculate the true range for the current date
    #             true_range = helper.true_range()
    #         else:
    #             current_price = helper.get_current_price()
    #             if current_price is not None:
    #                 true_range = current_price['high'] - current_price['low']
    #
    #         if true_range is None:
    #             return None
    #
    #         # Add the true range value to the list
    #         true_range_values.append(true_range)
    #
    #         # Move to the previous date
    #         date = helper.get_previous_row_by_date(date)['date']
    #
    #     # Create a pandas Series using the true range values
    #     true_range_series = pd.Series(true_range_values)
    #
    #     return true_range_series.mean()
