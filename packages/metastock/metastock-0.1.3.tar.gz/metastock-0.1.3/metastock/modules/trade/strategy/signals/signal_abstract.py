from abc import abstractmethod, ABC

from jsonschema.validators import validate

from metastock.modules.trade.error import NotSupportConfigType
from metastock.modules.trade.strategy.signals.input_schema import SIGNAL_INPUT_SCHEMA_V1, SIGNAL_INPUT_SCHEMA_V1_NAME
from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract


class SignalAbstract(ABC):
    strategy: StrategyAbstract | None
    name = None

    def __init__(self):
        self.strategy = None
        self.input_config = None

    def load_input(self, input_config: dict):
        api = input_config['api']

        if api == SIGNAL_INPUT_SCHEMA_V1_NAME:
            self._load_input_v1(input_config)
        else:
            raise NotSupportConfigType(f"Not support this config input api {api}")

    def _load_input_v1(self, input_config):
        try:
            validate(input_config, SIGNAL_INPUT_SCHEMA_V1)

            self.input_config = input_config
        except Exception as e:
            raise NotSupportConfigType(f"Wrong format of {SIGNAL_INPUT_SCHEMA_V1_NAME}")

    def get_input(self) -> dict:
        return self.input_config['input']

    def get_name(self):
        return self.name

    def set_strategy(self, strategy: StrategyAbstract):
        self.strategy = strategy

    def get_strategy(self) -> StrategyAbstract:
        if self.strategy is None:
            raise Exception('Please set strategy for signal before use')

        return self.strategy

    @abstractmethod
    def support_output_versions(self) -> list[str]:
        pass

    @abstractmethod
    def get_output(self, version = 'v1'):
        """
        Retrieves the output signal based on the specified version.

        Currently, only return hullma data for alerting

        Args:
            self (object): The instance of the class.
            version (str, optional): The version of the signal output to retrieve. Defaults to 'v1'.

        Returns:
            Union[SignalOutputV1, SignalOutputV2]: The signal output based on the specified version.

        Raises:
            None

        Example:
            SignalOutputV2(...)
        """
        pass
