from reactivex import compose, operators as ops

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.r.action import EMPTY
from metastock.modules.core.util.r.effect_base import EffectBase
from metastock.modules.core.util.r.rx_common import of_type
from metastock.modules.mbinance.um.r.actions.ac_001_market_data_update import (
    AC_001_MARKET_DATA_UPDATE,
)


class ReceiveKlineEffect(EffectBase):
    def __init__(self, logger: AppLogger):
        self._logger = logger

    def effect(self, _):
        def __map_to_empty(action):
            # self._logger.info(
            #     f"receive action payload {action.payload[['x', 'T', 'o', 'c']]}"
            # )
            return EMPTY

        return compose(of_type(AC_001_MARKET_DATA_UPDATE), ops.map(__map_to_empty))
