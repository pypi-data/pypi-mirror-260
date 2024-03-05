import arrow
import pandas as pd

from metastock.modules.com.technical_indicator.hullma import Hullma, HullmaConfig
from metastock.modules.core.util.app_error import AppError
from metastock.modules.stockinfo.ulti.get_price_history import get_price_history


class StockTradingAnalysisHullma:
    def __init__(self, symbol: str = None, price_history: list = None):
        self._price_history = price_history
        self.symbol = symbol

    def get_data(self):
        if self.symbol is None:
            raise AppError("Missing symbol data")

        price_history = self._get_price_history()
        hullma_config = HullmaConfig()
        hullma = Hullma(history=price_history, symbol=self.symbol)
        hullma.set_config(hullma_config)
        hullma_data = hullma.get_data()
        hullma_data_state, cur_gap_percent = self.calculate_state_hullma(hullma_data)

        # addition information for downtrend
        current_trend = hullma_data_state.iloc[0]["trend"]
        change_percent = 0
        day_in_down_trend = 0

        if current_trend == -1:
            beginning_last_up_trend_index = self._find_beginning_last_up_trend(
                hullma_data_state
            )
            if beginning_last_up_trend_index is not None:
                price_df = hullma.get_price_helper().get_df_after_date(
                    beginning_last_up_trend_index
                )
                max_price = price_df["high"].max()
                change_percent = round(
                    (
                        max_price / hullma.get_price_helper().get_df().iloc[0]["close"]
                        - 1
                    )
                    * 100
                )
            index_from_beginning_down_trend = self._find_beginning_current_down_trend(
                hullma_data_state
            )
            day_in_down_trend = hullma_data_state.index.get_loc(
                index_from_beginning_down_trend
            )

        data = {
            "l16_hullma_trend": int(current_trend),
            "l16_hullma_highest_diff_percent": int(change_percent),
            "l16_hullma_day_in_trend": int(day_in_down_trend),
            "cur_gap_percent": int(cur_gap_percent),
        }

        return data

    def _find_beginning_current_down_trend(self, df: pd.DataFrame):
        current_trend = df.iloc[0]["trend"]
        if current_trend == -1:
            for index, row in df.iterrows():
                _day_trend = row["trend"]
                if _day_trend == 1:
                    return index

        return None

    def _find_beginning_last_up_trend(self, df: pd.DataFrame, date_range=10):
        current_trend = df.copy(deep=True)[df["trend"] != 0].iloc[0]["trend"]
        last_up_trend = False
        total_date_range = 0
        if current_trend == -1:
            for index, row in df.iterrows():
                _day_trend = row["trend"]

                if _day_trend == 0:
                    continue
                if (
                    _day_trend == -1
                    and total_date_range >= date_range
                    and last_up_trend
                ):
                    return index
                if _day_trend == 1:
                    last_up_trend = True

                total_date_range = total_date_range + 1

        return None

    def _find_beginning_current_trend(self, df: pd.DataFrame):
        current_trend = df.copy(deep=True)[df["trend"] != 0].iloc[0]["trend"]
        for index, row in df.iterrows():
            _day_trend = row["trend"]

            if _day_trend == 0 or _day_trend == current_trend:
                continue

            return index

    def calculate_state_hullma(self, hullma_data: pd.Series, window=4):
        # hullma change qua cac ngay
        hullma_data_ca = hullma_data[::-1].diff()
        hullma_data_ca_avg = hullma_data_ca.abs().rolling(window=window).mean().shift(1)
        hullma_data_ca_abs = hullma_data_ca.abs()

        hullma_data_ca_ca = hullma_data_ca.diff().abs()
        hullma_data_ca_ca_avg = (
            hullma_data_ca_ca.abs().rolling(window=window).mean().shift(1)
        )

        # https://www.notion.so/vjcspy/Hullma-4f6d33f65c034a7b8424592d0c89c1cf?pvs=4
        # Can phai ket hop ca 2 yeu to de xac dinh state cua hullma
        condition_positive = (hullma_data_ca > 0) & (
            (hullma_data_ca_ca > 0.5 * hullma_data_ca_ca_avg)
            | (hullma_data_ca_abs > 0.5 * hullma_data_ca_avg)
        )
        condition_negative = (hullma_data_ca < 0) & (
            (hullma_data_ca_ca > 0.5 * hullma_data_ca_ca_avg)
            | (hullma_data_ca_abs > 0.5 * hullma_data_ca_avg)
        )

        # Create a DataFrame to store the result
        result_df = pd.DataFrame(index=hullma_data.index)
        result_df["trend"] = 0  # Initialize with 0

        result_df.loc[condition_positive, "trend"] = 1
        result_df.loc[condition_negative, "trend"] = -1

        # Check if value is not ceil and gap percent
        beginning_trend_date = self._find_beginning_current_trend(
            result_df.copy(deep=True)
        )
        hullma_data_ca_current = hullma_data_ca.abs()[hullma_data_ca.index.max()]
        hullma_data_ca_max_current_trend = hullma_data_ca.abs()[
            hullma_data_ca.index >= beginning_trend_date
        ].max()

        return result_df, round(
            hullma_data_ca_current * 100 / hullma_data_ca_max_current_trend
        )

    def _get_price_history(self):
        if self._price_history is None:
            current_date = arrow.now()
            from_date = current_date.shift(months=-6).format("YYYY-MM-DD")

            self._price_history = get_price_history(
                symbol=self.symbol,
                from_date=from_date,
                to_date=current_date.format("YYYY-MM-DD"),
            )

        return self._price_history

    def get_symbol(self):
        return self.symbol
