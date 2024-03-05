from pydantic import BaseModel, Extra
from pyrsistent import field, pmap, pmap_field, PRecord, pvector, pvector_field

from metastock.modules.core.logging.logger import get_logger
from metastock.modules.core.util.r.action import Action
from metastock.modules.mbinance.error.fatal_error import FatalError
from metastock.modules.mbinance.um.api_schema.event.account_update_event import (
    AccountUpdateEvent,
    PositionItem,
)
from metastock.modules.mbinance.um.api_schema.event.order_update_event import (
    OrderTradeUpdateEvent,
)
from metastock.modules.mbinance.um.api_schema.response.order import OrderResponse
from metastock.modules.mbinance.um.api_schema.response.position_info import PositionInfo
from metastock.modules.mbinance.um.r.actions.ac_003_account_balance_update import (
    AC_003_ACCOUNT_UPDATE,
)
from metastock.modules.mbinance.um.r.actions.ac_008_order_trade_update import (
    AC_008_ORDER_TRADE_UPDATE,
)
from metastock.modules.mbinance.um.r.actions.order.ac_025_create_tp_order_success import (
    AC_025_CREATE_TP_ORDER_SUCCESS,
)
from metastock.modules.mbinance.um.r.actions.order.position.ac_t02_get_position_success import (
    AC_T02_GET_POSITION_SUCCESS,
)
from metastock.modules.mbinance.um.r.actions.order.ac_022_create_new_pos_order_success import (
    AC_022_CREATE_NEW_POS_ORDER_SUCCESS,
)
from metastock.modules.mbinance.um.util.fmt_state_update_action import (
    fmt_state_update_action,
)
from metastock.modules.mbinance.um.value.trade_strategy_type import DecideInfo
from metastock.modules.mbinance.um.value.um_value import UMValue


class PositionState(BaseModel):
    # entryPrice: str
    # breakEvenPrice: str
    # marginType: str
    # isAutoAddMargin: bool
    # isolatedMargin: str
    # leverage: str
    # liquidationPrice: str
    # markPrice: str
    # maxNotionalValue: str
    positionAmt: str
    # notional: str
    # isolatedWallet: str
    symbol: str
    # unRealizedProfit: str
    positionSide: str
    updateTime: int

    class Config:
        extra = Extra.ignore  # Bỏ qua các trường thừa


class UmTradeState(PRecord):
    position = field(type=(PositionState, type(None)))

    order = field(type=(OrderResponse, type(None)))  # from create new order response
    client_order_id = field(type=(str, type(None)))

    tp_orders = pmap_field(
        int, OrderResponse
    )  # list các tp order from create new order response

    """
    - Include all order type
    - Not necessary for delete every has order update, because we will find by order_id
    """
    order_update_events = pvector_field(OrderTradeUpdateEvent)

    strategy_results = pmap_field(str, DecideInfo)


def um_trade_reducer(state: UmTradeState, action: Action) -> UmTradeState:
    if state is None:
        state = UmTradeState(
            position=None,
            order=None,
            client_order_id=None,
            tp_orders=pmap(),
            order_update_events=pvector(),
            strategy_results=pmap(),
        )

    if action is None:
        return state

    match action.name:
        case AC_022_CREATE_NEW_POS_ORDER_SUCCESS.name:
            state = state.set("order", action.payload)
            get_logger().info(
                fmt_state_update_action(AC_022_CREATE_NEW_POS_ORDER_SUCCESS.name)
            )

        case AC_025_CREATE_TP_ORDER_SUCCESS.name:
            order_update_event: OrderTradeUpdateEvent = action.payload.get(
                "order_update_event"
            )
            trade_id = order_update_event.order_info.trade_id
            tp_order: OrderResponse = action.payload.get("tp_order")
            tp_orders = state.get("tp_orders")
            existed_tp_orders = tp_orders.get(trade_id)

            if existed_tp_orders is not None:
                raise FatalError("tp_order already existed. Why???")

            state = state.set(
                "tp_orders",
                tp_orders.set(trade_id, tp_order),
            )
            get_logger().info(
                fmt_state_update_action(AC_025_CREATE_TP_ORDER_SUCCESS.name)
            )

        case AC_008_ORDER_TRADE_UPDATE.name:
            state = state.set(
                "order_update_events",
                state.get("order_update_events").append(action.payload),
            )
            get_logger().info(fmt_state_update_action(AC_008_ORDER_TRADE_UPDATE.name))

        case AC_T02_GET_POSITION_SUCCESS.name:
            position: PositionInfo = action.payload
            state = state.set("position", PositionState(**position.model_dump()))
            get_logger().info(
                f"{fmt_state_update_action(AC_T02_GET_POSITION_SUCCESS.name)} -> Updated positions info"
            )

        case AC_003_ACCOUNT_UPDATE.name:
            account_update: AccountUpdateEvent = action.payload
            positions = account_update.update_data.positions

            if len(positions) > 0:
                ps: list[PositionItem] = list(
                    filter(
                        lambda p: p.symbol == UMValue.SYMBOL(),
                        positions,
                    )
                )
                if len(ps) == 1:
                    state = state.set(
                        "position",
                        PositionState(
                            symbol=ps[0].symbol,
                            positionAmt=ps[0].position_amount,
                            positionSide=ps[0].position_side,
                            updateTime=account_update.event_time,
                        ),
                    )
                get_logger().info(
                    f"{fmt_state_update_action(AC_003_ACCOUNT_UPDATE.name)} -> Updated positions info"
                )

    return state
