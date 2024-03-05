from metastock.modules.trade.strategy.abstract_manager import AbstractManager


class AccessorManager(AbstractManager):
    INSTANCE = None


def accessor_manager() -> AccessorManager:
    if AccessorManager.INSTANCE is None:
        AccessorManager.INSTANCE = AccessorManager()

    return AccessorManager.INSTANCE
