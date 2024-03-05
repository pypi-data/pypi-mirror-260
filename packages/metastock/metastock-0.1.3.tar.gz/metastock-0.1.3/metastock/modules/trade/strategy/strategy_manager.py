from typing import Any

from metastock.modules.trade.strategy.abstract_manager import AbstractManager


class StrategyManager(AbstractManager):
    INSTANCE = None


def strategy_manager() -> StrategyManager:
    if StrategyManager.INSTANCE is None:
        StrategyManager.INSTANCE = StrategyManager()

    return StrategyManager.INSTANCE
