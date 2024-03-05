from abc import ABC, abstractmethod


class AbstractStockTradingAnalysis(ABC):
    def __init__(self, symbol: str, price_history: list = None):
        self._price_history = price_history
        self._symbol = symbol

    @abstractmethod
    def get_data(self):
        pass

    def get_price_history(self) -> list:
        return self._price_history if isinstance(self._price_history, list) else []

    def get_symbol(self):
        return self._symbol
