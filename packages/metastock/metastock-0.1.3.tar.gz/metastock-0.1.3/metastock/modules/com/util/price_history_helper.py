import pandas as pd
from datetime import datetime

from metastock.modules.com.schema.price_history_schema import priceHistorySchema
from metastock.modules.core.util.df_get_row_by_column_value import df_get_row_by_column_value
from metastock.modules.core.util.pd.pd_to_datetime import pd_to_datetime


def average_price(row):
    return (row['high'] + row['low']) / 2


class PriceHistoryHelper:
    """
       Helper class for working with price history data.
    """

    _date: str = datetime.today().strftime('%Y-%m-%d')
    _df: pd.DataFrame | None

    def __init__(self, data, skip_validate=False):

        if not skip_validate and isinstance(data, list) and len(data) > 0:
            priceHistorySchema.load(data[0])
        self._data = data
        self._df = None

    def _get_df(self):
        if self._df is None:
            df = pd.DataFrame(self._data)
            self._df = df.sort_values(by='date', ascending=False)
            self._df.reset_index(drop=True, inplace=True)

        return self._df.copy(deep=True)

    def _get_start_date(self, end_date, length):
        data_df = self._get_df()
        end_date = pd_to_datetime(end_date)
        data_df['date'] = pd_to_datetime(data_df['date'])
        data_df = data_df[data_df['date'] <= end_date]
        data_df = data_df.head(length)
        start_date = data_df.iloc[-1]['date']

        return start_date

    def _get_target_date_index(self, df_sorted: pd.DataFrame) -> int:
        target_date = self._date
        return df_sorted[df_sorted["date"] == target_date].index[0]

    def set_date(self, date: str):
        self._date = date

        return self

    def sma(self, length: int) -> float | None:
        df_sorted = self._get_df()
        idx = self._get_target_date_index(self._get_df())

        if idx + length > len(df_sorted):
            return None

        sma_data = df_sorted.iloc[idx:idx + length]

        return sma_data["close"].mean()

    def sma_by_source_func(self, length: int, cal_source_func=lambda row: row['close']) -> float | None:
        df_sorted = self._get_df()
        idx = self._get_target_date_index(df_sorted)

        if idx + length > len(df_sorted):
            return None

        sma_data = df_sorted.iloc[idx:idx + length]
        transformed_data = sma_data.apply(cal_source_func, axis=1)

        return transformed_data.mean()

    def stdev(self, length: int, cal_source_func=lambda row: row['close']):
        """
        Calculate the standard deviation of a specific data source over a given length.

        Args:
            length: The length of the data range.
            cal_source_func: The function to transform the data (default: lambda row: row['close']).

        Returns:
            The standard deviation of the transformed data, or None if the length is invalid.
        """
        df = self._get_df()
        date = self._date
        df['date'] = pd_to_datetime(df['date'])
        end_date = pd_to_datetime(date)
        start_date = self._get_start_date(self._date, length)

        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        if len(filtered_df) != length:
            return None

        # Sử dụng hàm func để biến đổi dữ liệu
        transformed_data = filtered_df.apply(cal_source_func, axis=1)

        return transformed_data.std()

    def get_previous_close(self, days: int = 1):
        return self.get_previous_close_by_date(self._date, days)

    def get_previous_close_by_date(self, date: str, days: int = 1) -> float | None:
        df = self._get_df()

        # Find the index of the target date
        idx = df[df['date'] == date].index

        if len(idx) == 0 or len(df) <= idx[0] + days:
            return None

        # Get the previous close value
        prev_close = df.loc[idx[0] + days, 'close']

        return prev_close

    def get_previous_row_by_date(self, date: str, days: int = 1) -> pd.Series | None:
        df = self._get_df()

        # Find the index of the target date
        idx = df[df['date'] == date].index

        if len(idx) == 0 or len(df) <= idx[0] + days:
            return None

        # Get the close value of the previous row
        prev = df.loc[idx[0] + days]

        return prev

    def get_subset_rows_by_date(self, date: str, days: int = 1) -> pd.DataFrame | None:
        df = self._get_df()

        # Find the index of the target date
        idx = df[df['date'] == date].index

        if len(idx) == 0 or len(df) < idx[0] + days:
            return None

        # Get the close value of the previous row
        subset_rows = df.loc[idx[0]: idx[0] + days - 1]

        return subset_rows

    def tr(self):
        return self.true_range()

    def true_range(self):
        return self.true_range_by_date(self._date)

    def true_range_by_date(self, date: str) -> float | None:
        df = self._get_df()

        # Find the row with the target date
        target_row = df[df['date'] == date]

        if len(target_row) == 0:
            return None

        # Calculate the True Range using the high, low, and previous close values
        high = target_row['high'].values[0]
        low = target_row['low'].values[0]
        prev_close = self.get_previous_close_by_date(date)

        if prev_close is None:
            return None

        return max(high - low, abs(high - prev_close), abs(low - prev_close))

    def get_current_price(self):
        return df_get_row_by_column_value(self._get_df(), 'date', self._date)

    def get_row_data_by_source_func(self, cal_source_func=lambda row: row['close']):
        """
        Get the transformed data for the current target date using a custom source function.

        Args:
            cal_source_func: The function to transform the data (default: lambda row: row['close']).

        Returns:
            The transformed data for the current target date, or None if the data is not available.
        """
        row = self.get_current_price()

        if row is not None:
            return cal_source_func(row)

        return None
