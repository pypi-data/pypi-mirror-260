from reactivex import compose, operators as ops

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.r.action import Action
from metastock.modules.core.util.r.effect_base import EffectBase
from metastock.modules.core.util.r.r_manager import RManager
from metastock.modules.core.util.r.rx_common import of_type
from metastock.modules.mbinance.exchange.connector.base.api_order_connector_base import (
    ApiOrderConnectorBase,
)
from metastock.modules.mbinance.um.api_schema.event.order_update_event import (
    OrderTradeUpdateEvent,
    OrderTradeUpdateInfo,
)
from metastock.modules.mbinance.um.r.actions.order.ac_024_create_tp_order import (
    AC_024_CREATE_TP_ORDER,
)
from metastock.modules.mbinance.um.r.actions.order.ac_025_create_tp_order_success import (
    AC_025_CREATE_TP_ORDER_SUCCESS,
)
from metastock.modules.mbinance.um.r.actions.order.ac_026_create_tp_order_error import (
    AC_026_CREATE_TP_ORDER_ERROR,
)
from metastock.modules.mbinance.um.value.um_order_type import OrderSide
from metastock.modules.mbinance.um.value.um_value import UMValue


class CreateTPOrderEffect(EffectBase):
    def __init__(self, logger: AppLogger, api_order_connector: ApiOrderConnectorBase):
        self._api_order_connector = api_order_connector
        self._logger = logger

    def effect(self, r: RManager):
        def __create_tp_order(action: Action):
            order_update_event: OrderTradeUpdateEvent = action.payload
            try:
                order_info: OrderTradeUpdateInfo = order_update_event.order_info
                symbol = order_info.symbol
                qty = order_info.last_filled_quantity
                side = (
                    OrderSide.BUY
                    if order_info.side == OrderSide.SELL.value
                    else OrderSide.SELL
                )
                if order_info.side == OrderSide.SELL.value:
                    price = round(
                        order_info.average_price
                        * (100 - UMValue.TP_PRICE_PERCENT)
                        / 100,
                        4,
                    )
                else:
                    price = round(
                        order_info.average_price
                        * (100 + UMValue.TP_PRICE_PERCENT)
                        / 100,
                        4,
                    )
                self._logger.info(
                    ">>> Creating 'TP Order' with symbol '{}', quantity '{}', side '{}', tp price '{}', origin avg "
                    "price '{}'".format(
                        symbol, qty, side, price, order_info.average_price
                    )
                )
                tp_order = self._api_order_connector.create_limit_order(
                    client_order_id=f"tp_{order_info.trade_id}",
                    symbol=symbol,
                    qty=qty,
                    side=side,
                    price=price,
                    reduce_only=True,
                )

                self._logger.info("OK create TP Order {}".format(tp_order))

                return AC_025_CREATE_TP_ORDER_SUCCESS(
                    {"order_update_event": order_update_event, "tp_order": tp_order}
                )
            except Exception as e:
                self._logger.exception(e, "Error creating tp order")

                return AC_026_CREATE_TP_ORDER_ERROR(
                    {"order_update_event": order_update_event, "error": e}
                )

        return compose(of_type(AC_024_CREATE_TP_ORDER), ops.map(__create_tp_order))
