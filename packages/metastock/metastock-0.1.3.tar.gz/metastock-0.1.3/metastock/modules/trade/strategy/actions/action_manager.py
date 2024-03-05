from metastock.modules.trade.strategy.abstract_manager import AbstractManager


class ActionManager(AbstractManager):
    INSTANCE = None


def action_manager() -> ActionManager:
    if ActionManager.INSTANCE is None:
        ActionManager.INSTANCE = ActionManager()

    return ActionManager.INSTANCE
