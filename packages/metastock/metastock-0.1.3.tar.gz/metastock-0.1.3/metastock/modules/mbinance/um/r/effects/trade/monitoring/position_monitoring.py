from reactivex import compose, operators as ops
from rich.panel import Panel
from rich.text import Text

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.r.action import Action, EMPTY
from metastock.modules.core.util.r.effect_base import EffectBase
from metastock.modules.core.util.r.r_manager import RManager
from metastock.modules.core.util.r.rx_common import of_type
from metastock.modules.mbinance.um.r.actions.ac_003_account_balance_update import (
    AC_003_ACCOUNT_UPDATE,
)
from metastock.modules.mbinance.um.r.actions.order.position.ac_t02_get_position_success import (
    AC_T02_GET_POSITION_SUCCESS,
)
from metastock.modules.mbinance.um.r.reducer.um_trade_reducer import (
    PositionState,
    UmTradeState,
)


class PositionMonitoringEffect(EffectBase):
    def __init__(self, logger: AppLogger):
        self._logger = logger

    def effect(self, r: RManager):
        def __monitoring_position(_: Action):
            trade_state: UmTradeState = r.get_state().get("trade")
            position: PositionState = trade_state.position
            self._logger.info(f"Current position {trade_state.position}")
            self._logger.console().print(
                Panel(
                    Text(
                        f"{position.positionAmt}",
                        justify="center",
                    ),
                    title="Position",
                )
            )
            return EMPTY

        return compose(
            of_type(AC_T02_GET_POSITION_SUCCESS, AC_003_ACCOUNT_UPDATE),
            ops.map(__monitoring_position),
        )
