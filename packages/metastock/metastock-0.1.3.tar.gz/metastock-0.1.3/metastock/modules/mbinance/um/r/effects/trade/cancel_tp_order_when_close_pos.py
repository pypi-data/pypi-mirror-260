from reactivex import compose, operators as ops

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.r.action import Action, EMPTY
from metastock.modules.core.util.r.effect_base import EffectBase
from metastock.modules.core.util.r.rx_common import of_type
from metastock.modules.mbinance.um.api_schema.event.account_update_event import (
    AccountUpdateEvent,
    PositionItem,
)
from metastock.modules.mbinance.um.exchange.connector.api_order_connector import (
    UMApiOrderConnector,
)
from metastock.modules.mbinance.um.r.actions.ac_003_account_balance_update import (
    AC_003_ACCOUNT_UPDATE,
)
from metastock.modules.mbinance.um.value.um_value import UMValue


class CancelTPOrderWhenClosePosEffect(EffectBase):
    def __init__(self, logger: AppLogger, api_order_connector: UMApiOrderConnector):
        self._logger = logger
        self._api_order_connector = api_order_connector

    def effect(self, r):
        def __cancel_tp_order_when_close_pos(action: Action):
            account_update: AccountUpdateEvent = action.payload
            positions = account_update.update_data.positions
            symbol = UMValue.SYMBOL()

            if not positions or len(positions) == 0:
                return EMPTY

            ps: list[PositionItem] = list(
                filter(lambda p: p.symbol == symbol, positions)
            )
            self._logger.info(f"positions: {ps}")
            if len(ps) != 1 or float(ps[0].position_amount) != 0:
                return EMPTY

            self._logger.info("Position was closed. Will cancel TP order if necessary")

            orders = self._api_order_connector.get_current_open_orders(symbol=symbol)

            if len(orders) == 0:
                self._logger.info(f"No open orders found. Skipping cancel TP Order")
                return EMPTY

            self._logger.info("TP Orders: %s", orders)

            # Hiện tại đã đặt TP order với config reduce only nên sẽ không lo khi close position mà vẫn còn TP order
            self._logger.error("Not yet implemented cancel TP order")
            return EMPTY

        return compose(
            of_type(AC_003_ACCOUNT_UPDATE), ops.map(__cancel_tp_order_when_close_pos)
        )
