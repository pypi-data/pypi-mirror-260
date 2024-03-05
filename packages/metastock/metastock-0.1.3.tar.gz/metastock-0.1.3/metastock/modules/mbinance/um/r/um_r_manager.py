from typing import List

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.r.combine_reducer import combine_reducer
from metastock.modules.core.util.r.effect_base import EffectBase
from metastock.modules.core.util.r.r_manager import RManager
from metastock.modules.mbinance.um.r.reducer.um_account_reducer import (
    um_account_reducer,
)
from metastock.modules.mbinance.um.r.reducer.um_common_reducer import um_common_reducer
from metastock.modules.mbinance.um.r.reducer.um_market_reducer import um_market_reducer
from metastock.modules.mbinance.um.r.reducer.um_trade_reducer import um_trade_reducer


class UMRManager(RManager):
    def __init__(
        self,
        effects: List[EffectBase],
        logger: AppLogger,
        combined_reducer=combine_reducer(
            {
                "common": um_common_reducer,
                "account": um_account_reducer,
                "market": um_market_reducer,
                "trade": um_trade_reducer,
            }
        ),
    ):
        super().__init__(combined_reducer, logger=logger)
        self.effects(*effects)
