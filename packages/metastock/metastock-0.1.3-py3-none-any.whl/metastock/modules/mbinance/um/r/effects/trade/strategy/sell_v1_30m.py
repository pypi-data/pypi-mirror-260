from reactivex import compose, operators as ops

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.r.action import Action, EMPTY
from metastock.modules.core.util.r.effect_base import EffectBase
from metastock.modules.core.util.r.rx_common import of_type
from metastock.modules.mbinance.um.r.actions.ac_001_market_data_update import (
    AC_001_MARKET_DATA_UPDATE,
)
from metastock.modules.mbinance.um.r.actions.order.strategy.ac_040_update_strategy_decide import (
    AC_040_UPDATE_STRATEGY_DECIDE,
)
from metastock.modules.mbinance.um.trade.strategy.config.sell_strategy_v1_config import (
    SellStrategyV1Config,
)
from metastock.modules.mbinance.um.trade.strategy.sell.msell_v1 import MSellV1Strategy
from metastock.modules.mbinance.value.common import TimeInterval


class SellStrategyV1ThirtyMinuteEffect(EffectBase):
    """
    Dựa vào sell v1 strategy để đưa ra quyết định xem có vào lệnh hay không?
    """

    def __init__(self, logger: AppLogger):
        self._logger = logger

    def __process_strategy(self, action: Action):
        if (
            not isinstance(action.payload, dict)
            or action.payload.get("kline_data") is None
        ):
            return EMPTY
        kline_data: dict = action.payload.get("kline_data")
        interval = kline_data.get("interval")

        if interval != TimeInterval.THIRTY_MINUTES.value:
            return EMPTY

        kline = kline_data.get("kline")

        strategy_config = SellStrategyV1Config(
            tp=0.2,
            sl=0.1,
            wt_diff_check=[2, 4],
            wt1_check=[4],
            hull_diff_check=[20, 20],
            hull_check=[-20, 20],
            is_check_hull=True,
        )
        msell_v1 = MSellV1Strategy(kline=kline, strategy_config=strategy_config)

        decide = msell_v1.run()

        return AC_040_UPDATE_STRATEGY_DECIDE(
            {"decide": decide, "type": f"{MSellV1Strategy.__STRATEGY_NAME__}_30m"}
        )

    def effect(self, r):
        return compose(
            of_type(AC_001_MARKET_DATA_UPDATE), ops.map(self.__process_strategy)
        )
