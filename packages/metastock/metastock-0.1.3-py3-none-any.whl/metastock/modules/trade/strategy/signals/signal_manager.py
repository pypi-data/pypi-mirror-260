from metastock.modules.trade.strategy.abstract_manager import AbstractManager


class SignalManager(AbstractManager):
    INSTANCE = None


def signal_manager() -> SignalManager:
    if SignalManager.INSTANCE is None:
        SignalManager.INSTANCE = SignalManager()

    return SignalManager.INSTANCE
