from metastock.modules.trade.strategy.abstract_manager import AbstractManager


class FilterManager(AbstractManager):
    INSTANCE = None


def filter_manager() -> FilterManager:
    if FilterManager.INSTANCE is None:
        FilterManager.INSTANCE = FilterManager()

    return FilterManager.INSTANCE
