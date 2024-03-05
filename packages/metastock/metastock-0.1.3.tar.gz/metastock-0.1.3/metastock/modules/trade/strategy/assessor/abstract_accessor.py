import json
import os
from abc import ABC, abstractmethod

from jsonschema.validators import validate

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.app_error import AppError
from metastock.modules.stockinfo.ulti.get_price_history import get_price_history
from metastock.modules.trade.error import NotSupportConfigType, TradeFileNotFoundError
from metastock.modules.trade.strategy.assessor.input_schema import (
    ACCESSOR_INPUT_SCHEMA_V1,
    ACCESSOR_INPUT_SCHEMA_V1_NAME,
)
from metastock.modules.trade.strategy.strategy_abstract import TradingStrategyState
from metastock.modules.trade.util.get_strategy_process_actions import (
    get_strategy_process_actions,
)
from metastock.modules.trade.util.get_strategy_processes import get_strategy_processes


class AbstractAccessor(ABC):
    name = None

    def __init__(self):
        self._completed_processes = []
        self._trading_strategy_processes = None
        self._strategy_data = None
        self._strategy_hash = None

    def set_strategy_hash(self, strategy_hash: str):
        self._strategy_hash = strategy_hash

    def get_strategy_hash(self):
        return self._strategy_hash

    def before_run(self):
        pass

    def run(self):
        self.before_run()

        self._strategy_data = get_strategy_processes(
            strategy_hash=self.get_strategy_hash()
        )
        self._trading_strategy_processes = self._strategy_data.get(
            "trading_strategy_process"
        )
        if isinstance(self._trading_strategy_processes, list):
            self._completed_processes = [
                item
                for item in self._trading_strategy_processes
                if (
                    item["state"] == TradingStrategyState.Complete.value
                    or item["state"] == TradingStrategyState.OutScope.value
                )
            ]
        else:
            raise AppError("Response data is wrong format")

        if len(self._completed_processes) < len(self._trading_strategy_processes):
            Logger().warning(
                f"Strategy process hasn't completed {len(self._completed_processes)}/{ len(self._trading_strategy_processes)}"
            )
        else:
            Logger().will(
                f"run accessor for '{len(self._completed_processes)}' completed strategy process with hash {self.get_strategy_hash()} "
            )

        for strategy_process in self._completed_processes:
            self.process_accessor_for_symbol(strategy_process=strategy_process)

    def process_accessor_for_symbol(self, strategy_process):
        Logger().will(f'process accessor for symbol {strategy_process["symbol"]}')
        history_price = get_price_history(
            symbol=strategy_process["symbol"], from_date=self._strategy_data["from"]
        )

        Logger().will(
            f"get strategy process actions for symbol {strategy_process['symbol']}"
        )
        process_actions = get_strategy_process_actions(
            strategy_hash=self.get_strategy_hash(), symbol=strategy_process["symbol"]
        )

        if "trading_strategy_action" in process_actions:
            process_actions = process_actions["trading_strategy_action"]
        else:
            raise AppError("Wrong data format process_actions")

        if len(process_actions) > 0:
            self.access(
                strategy_process=strategy_process,
                history_price=history_price,
                process_actions=process_actions,
            )
        else:
            Logger().info(
                f"Dont have any action for symbol {strategy_process['symbol']}"
            )

    @abstractmethod
    def access(self, strategy_process, process_actions, history_price):
        pass

    def get_input_full_path(self, input_path: str):
        return f"fixture/trade/predefined_inputs/accessor/{input_path}"

    def load_input(self, input_file: str = None):
        if input_file is None or input_file == "":
            Logger().will("use default config file because user not pass input config")
            input_file = self.get_input_full_path(f"{self.name}/default.json")
        else:
            input_file = self.get_input_full_path(input_file)

        # Lấy đường dẫn của thư mục project. Giả sử thư mục project của bạn là thư mục cha của thư mục 'src'
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", input_file)
        )
        Logger().info(f"Load input of accessor by path: {file_path}")
        if not os.path.exists(file_path):
            Logger().error("Not found input config file")
            raise TradeFileNotFoundError()

        with open(file_path, "r") as file:
            input_config = json.load(file)

        api = input_config["api"]

        if api == ACCESSOR_INPUT_SCHEMA_V1_NAME:
            self._load_input_v1(input_config)
        else:
            raise NotSupportConfigType(f"Not support this config input api {api}")

        self.after_load_input()

    def _load_input_v1(self, input_config):
        try:
            validate(input_config, ACCESSOR_INPUT_SCHEMA_V1)
            self._input_config = input_config
            Logger().info(f"Accessor config {input_config}")
        except Exception as e:
            raise NotSupportConfigType(
                f"Wrong format of {ACCESSOR_INPUT_SCHEMA_V1_NAME}"
            )

    def after_load_input(self):
        pass

    def get_input_config(self):
        return self._input_config
