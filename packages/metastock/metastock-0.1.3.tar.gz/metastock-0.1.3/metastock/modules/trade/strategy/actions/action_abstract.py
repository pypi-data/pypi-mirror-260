from abc import ABC, abstractmethod

from jsonschema.validators import validate

from metastock.modules.core.util.find_common_elements import find_common_elements
from metastock.modules.trade.error import NotSupportConfigType
from metastock.modules.trade.strategy.actions.input_schema import ACTION_INPUT_SCHEMA_V1, ACTION_INPUT_SCHEMA_V1_NAME
from metastock.modules.trade.strategy.signals.signal_abstract import SignalAbstract
from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract


class ActionAbstract(ABC):
    strategy: StrategyAbstract | None
    name = None

    def __init__(self):
        self.strategy = None

    def load_input(self, input_config: dict):
        api = input_config['api']

        if api == ACTION_INPUT_SCHEMA_V1_NAME:
            return self._load_input_v1(input_config)

        raise NotSupportConfigType(f"Not support this config input api {api}")

    def _load_input_v1(self, input_config):
        try:
            validate(input_config, ACTION_INPUT_SCHEMA_V1)
        except Exception as e:
            raise NotSupportConfigType(f"Wrong format of {ACTION_INPUT_SCHEMA_V1_NAME}")

    def get_name(self):
        return self.name

    @abstractmethod
    def support_signal_output_versions(self) -> list[str]:
        pass

    @abstractmethod
    def run(self, strategy: StrategyAbstract, signals: list[SignalAbstract]):
        pass

    def _get_compatible_versions(self, signal: SignalAbstract):
        return find_common_elements(self.support_signal_output_versions(), signal.support_output_versions())

    def set_strategy(self, strategy: StrategyAbstract):
        self.strategy = strategy

    def get_strategy(self) -> StrategyAbstract:
        if self.strategy is None:
            raise Exception('Please set strategy for signal before use')

        return self.strategy
