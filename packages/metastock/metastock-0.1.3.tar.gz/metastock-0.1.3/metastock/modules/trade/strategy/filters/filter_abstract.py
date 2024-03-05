from abc import ABC, abstractmethod
from enum import Enum

from jsonschema.validators import validate

from metastock.modules.trade.error import NotSupportConfigType
from metastock.modules.trade.strategy.filters.input_schema import (
    FILTER_INPUT_SCHEMA_V1,
    FILTER_INPUT_SCHEMA_V1_NAME,
)
from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract


class FilterType(Enum):
    GLOBAL = 1
    DAY = 2


class FilterAbstract(ABC):
    strategy: StrategyAbstract | None
    name = None

    def __init__(self):
        self.strategy = None
        self.type = FilterType.GLOBAL
        self._input_config = None

    def get_name(self):
        return self.name

    def get_type(self) -> FilterType:
        return self.type

    # @abstractmethod
    # def filter(self, symbol: str) -> bool:
    #     pass

    @abstractmethod
    def get_allowable_list(self) -> list[str]:
        pass

    def load_input(self, input_config: dict):
        api = input_config["api"]

        if api == FILTER_INPUT_SCHEMA_V1_NAME:
            return self._load_input_v1(input_config)

        raise NotSupportConfigType(f"Not support this config input api {api}")

    def _load_input_v1(self, input_config):
        try:
            validate(input_config, FILTER_INPUT_SCHEMA_V1)
            self._input_config = input_config
        except Exception as e:
            raise NotSupportConfigType(f"Wrong format of {FILTER_INPUT_SCHEMA_V1_NAME}")

    def get_input(self):
        return self._input_config.get("input")

    def set_strategy(self, strategy: StrategyAbstract):
        self.strategy = strategy

    def get_strategy(self) -> StrategyAbstract:
        if self.strategy is None:
            raise Exception("Please set strategy for signal before use")

        return self.strategy
