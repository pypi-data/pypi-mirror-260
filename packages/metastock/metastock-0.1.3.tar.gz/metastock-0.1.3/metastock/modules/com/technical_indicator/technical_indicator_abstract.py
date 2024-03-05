from abc import ABC

import arrow

from metastock.modules.com.helper.price_history_df_helper import PriceHistoryDfHelper
from metastock.modules.com.technical_indicator.error import (
    ConfigNotSetError,
    DateNotSetError,
)
from metastock.modules.stockinfo.ulti.get_price_history import get_price_history


class TechnicalIndicatorAbstract(ABC):
    _price_history_df_helper: PriceHistoryDfHelper | None

    def __init__(self, history: list = None, symbol: str = None):
        self._date = None
        self._price_history_df_helper = None
        self._history = history
        self._symbol = symbol
        self._config = None

    def set_config(self, config):
        self._config = config

        return self

    def get_config(self):
        return self._config

    def get_date(self):
        return self._date

    def set_date(self, date: str):
        self._date = date

        return self

    def get_price_helper(self, skip_validate=False) -> PriceHistoryDfHelper:
        if self._price_history_df_helper is None:
            self._price_history_df_helper = PriceHistoryDfHelper(
                data=self.get_history(), skip_validate=skip_validate
            )

        return self._price_history_df_helper

    def get_history(self):
        if self._history is None:
            current_date = arrow.now()
            from_date = current_date.shift(months=-6).format("YYYY-MM-DD")

            self._history = get_price_history(
                symbol=self.get_symbol(),
                from_date=from_date,
                to_date=current_date.format("YYYY-MM-DD"),
            )

        return self._history

    def get_symbol(self):
        return self._symbol

    def get_data(self):
        if self._date is None:
            raise DateNotSetError()

        if self.get_config() is None:
            raise ConfigNotSetError()

    def get_data_for_date(self, date: str):
        self._date = date

        return self.get_data()
