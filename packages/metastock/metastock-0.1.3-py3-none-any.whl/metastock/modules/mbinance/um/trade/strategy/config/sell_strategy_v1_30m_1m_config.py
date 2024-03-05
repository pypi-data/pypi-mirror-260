from metastock.modules.mbinance.um.trade.strategy.config.sell_strategy_v1_config import (
    SellStrategyV1Config,
)


class SellStrategyV130m1mConfig:
    def __init__(
        self,
        strategy_config_30m: SellStrategyV1Config,
        strategy_config_1m: SellStrategyV1Config,
    ):
        self._strategy_config_30m = strategy_config_30m
        self._strategy_config_1m = strategy_config_1m

    def get_strategy_config_30m(self) -> SellStrategyV1Config:
        return self._strategy_config_30m

    def get_strategy_config_1m(self) -> SellStrategyV1Config:
        return self._strategy_config_1m
