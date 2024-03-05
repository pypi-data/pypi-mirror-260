import os
from typing import Any

import jsonschema
import simplejson as json

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.http_client import http_client
from metastock.modules.trade.error import (
    CouldNotResolveUrlConfig,
    StrategyNotFound,
    TradeFileNotFoundError,
)
from metastock.modules.trade.generator.input_schema import PRE_DEFINED_INPUT_SCHEMA_V1
from metastock.modules.trade.generator.strategy_generator_abstract import (
    StrategyGeneratorAbstract,
)
from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract
from metastock.modules.trade.strategy.strategy_manager import strategy_manager
from metastock.modules.trade.util.get_strategy_hash import get_strategy_hash
from metastock.modules.trade.value.url import TradeUrlValue


class PredefinedStrategyGenerator(StrategyGeneratorAbstract):
    logger = Logger()

    def __init__(self, predefined_input: str):
        super().__init__()
        self.predefined_input = predefined_input
        self._load_input()

    def _load_input(self):
        # Lấy đường dẫn của thư mục project. Giả sử thư mục project của bạn là thư mục cha của thư mục 'src'
        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "..", self.predefined_input
            )
        )
        self.logger.info(f"Load input of generator by path: {file_path}")
        if not os.path.exists(file_path):
            raise TradeFileNotFoundError()

        with open(file_path, "r") as file:
            data = json.load(file)

        if data is not None:
            api = data["api"]
            match api:
                case "@predefined_input/generator/v1":
                    return self._load_input_v1(data)

    def _load_input_v1(self, data: Any):
        # Validate input
        jsonschema.validate(data, PRE_DEFINED_INPUT_SCHEMA_V1)

        # load strategy
        self._load_input_strategy_v1(data["strategy"])

    def _load_input_strategy_v1(self, strategy_config):
        # check if there is a strategy with that name
        self.strategy_name = strategy_config["name"]
        if strategy_manager().get_class_map().get(self.strategy_name) is not None:
            try:
                self.strategy_class = (
                    strategy_manager()
                    .get_class_map()
                    .get(strategy_config["name"])["class"]
                )
                self.strategy: StrategyAbstract = self.strategy_class()
            except Exception:
                pass

        if self.strategy is None:
            raise StrategyNotFound()

        # if the configuration was set by files type
        if strategy_config["input"]["type"] == "files":
            self.strategy_inputs_type = "files"
            self.strategy_inputs = self._load_input_strategy_files_v1(strategy_config)

    def _load_input_strategy_files_v1(self, strategy_config):
        if not isinstance(strategy_config["input"]["data"], list):
            return
        _input_configs = []
        for _file in strategy_config["input"]["data"]:
            file_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "..", _file)
            )
            if not os.path.exists(file_path):
                raise TradeFileNotFoundError("Not found strategy input configuration")
            with open(file_path, "r") as file:
                data = json.load(file)
                _input_configs.append({"file": _file, "data": data})

        return _input_configs

    def generate(self):
        self.logger.info(
            f"Process generate with strategy '{self.strategy_name}' and input type '{self.strategy_inputs_type}' "
        )
        self.logger.debug(f"strategy inputs data {self.strategy_inputs}")
        client = http_client()
        url = TradeUrlValue.TRADING_STRATEGY_PROCESS_URL

        if url is None:
            raise CouldNotResolveUrlConfig()

        # call api service to generate jobs for strategy and it's inputs
        self.logger.info(f"Size of strategy inputs {len(self.strategy_inputs)}")
        for config in self.strategy_inputs:
            self.logger.info(
                f"Process strategy '{self.strategy_name}' with input name '{config.get('data').get('name')}'"
            )
            self.logger.info(
                f"Will simulate load strategy '{self.strategy_name}' for validate input"
            )
            strategy: StrategyAbstract = self.strategy_class()
            strategy.load_input(input_config=config["data"])
            self.logger.ok(
                f"validate input for strategy [blue]{config['data']['name']}[/blue]"
            )

            strategy_input = config["data"]["input"]
            from_date, to_date = self._get_range_data(strategy_input["range"])
            hash_key = get_strategy_hash(
                strategy_name=self.strategy_name,
                strategy_input=config["data"],
                from_date=from_date,
                to_date=to_date,
            )

            meta = {"allowable_list": strategy.get_allowable_list()}

            data = {
                "strategy_name": self.strategy_name,
                "from_date": from_date,
                "to_date": to_date,
                "strategy_input": config["data"],
                "hash_key": hash_key,
                "meta": meta,
            }

            try:
                self.logger.info(f"Will send to API server to process strategy")
                self.logger.debug(f"request data {data}")
                res = client.post(url, data)

                if res.status_code == 409:
                    self.logger.warning(
                        f"[yellow]DUPLICATED[/yellow] Already generated for strategy '{self.strategy_name}' and "
                        f"input name '{config['data']['name']}'"
                    )
                elif res.status_code == 201 or res.status_code == 200:
                    res_json = res.json()
                    if "data" in res_json:
                        hash_key = res_json["data"]["hash"]

                    self.logger.info(
                        f"[green]OK[/green] generated for strategy '{self.strategy_name}' and input name '{config['data']['name']}' with hash '{hash_key}'"
                    )
                else:
                    self.logger.warning(
                        f"Could not generate in api server with response {res.text}"
                    )
            except Exception as e:
                self.logger.error(
                    "An error occurred when send to downstream: %s",
                    e,
                )
