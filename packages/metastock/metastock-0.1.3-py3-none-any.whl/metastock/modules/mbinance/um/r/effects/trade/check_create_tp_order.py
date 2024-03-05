from reactivex import compose, operators as ops

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.r.action import Action, EMPTY
from metastock.modules.core.util.r.effect_base import EffectBase
from metastock.modules.core.util.r.rx_common import of_type
from metastock.modules.mbinance.um.api_schema.event.order_update_event import (
    OrderTradeUpdateEvent,
)
from metastock.modules.mbinance.um.r.actions.ac_008_order_trade_update import (
    AC_008_ORDER_TRADE_UPDATE,
)
from metastock.modules.mbinance.um.r.actions.order.ac_024_create_tp_order import (
    AC_024_CREATE_TP_ORDER,
)
from metastock.modules.mbinance.um.value.um_order_type import OrderStatus


class CheckCreateTPOrderEffect(EffectBase):
    def __init__(self, logger: AppLogger):
        self._logger = logger

    def effect(self, r):
        """
        - Lưu ý là không chỉ có một TP order. Mỗi lần order được filled (có thể sẽ là partial fill hoặc fulfill) thì
        sẽ tạo một TP order tương ứng
        - Sẽ map XXX của order update với TP order

        :param r:
        :return:
        """

        def __is_update_order(order_update: OrderTradeUpdateEvent):
            # TODO: sửa lại điều kiện này, hiện tại do market đang fix order được tạo có prefix là web nên có thể tạm
            #  sử dụng cơ chế này
            return (
                order_update.order_info.client_order_id.startswith("web_")
                or order_update.order_info.client_order_id
                == r.get_state().get("trade").client_order_id
            ) and order_update.order_info.is_reduce_only == False

        def __check_if_create_tp_order(action: Action):
            order_update: OrderTradeUpdateEvent = action.payload
            if not __is_update_order(order_update):
                return EMPTY

            if order_update.order_info.order_status not in [
                OrderStatus.FILLED.value,
                OrderStatus.PARTIALLY_FILLED.value,
            ]:
                return EMPTY

            self._logger.info(
                ">>> All conditions is passed. Will trigger to create tp order"
            )

            return AC_024_CREATE_TP_ORDER(order_update)

        return compose(
            of_type(AC_008_ORDER_TRADE_UPDATE), ops.map(__check_if_create_tp_order)
        )
