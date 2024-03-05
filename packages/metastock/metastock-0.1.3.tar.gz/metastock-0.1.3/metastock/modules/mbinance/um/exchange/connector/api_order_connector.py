from typing import List

from metastock.modules.mbinance.exchange.connector.base.api_order_connector_base import (
    ApiOrderConnectorBase,
)
from metastock.modules.mbinance.um.api_schema.response.order import OrderResponse
from metastock.modules.mbinance.um.util.get_client import get_um_client
from metastock.modules.mbinance.um.value.um_order_type import (
    OrderPriceMatch,
    OrderSide,
    OrderTimeInForce,
    OrderType,
    OrderWorkingType,
)


class UMApiOrderConnector(ApiOrderConnectorBase):
    def stop(self):
        pass

    def create_sl_order(
        self,
        client_order_id: str,
        symbol: str,
        side: OrderSide,
        stop_price: float,
        qty: float,
        price: float = None,
    ):
        self._logger.will("creating new stop loss order: {}".format(symbol))
        client = get_um_client()

        order_data = {
            "newClientOrderId": client_order_id,
            "symbol": symbol,
            "side": side.value,  # Mua hoặc bán
            # "positionSide": OrderPositionSide.LONG.value,
            "type": OrderType.STOP.value,  # Loại lệnh TRAILING_STOP_MARKET
            "timeInForce": OrderTimeInForce.GTC.value,  # Loại thời gian hiệu lực GTD
            "quantity": qty,  # Số lượng
            "price": price,  # TODO: priceMatch
            "stopPrice": stop_price,  # Giá dừng (Stop Price)
            # "closePosition": false,  # Không đóng tất cả vị trí
            "workingType": OrderWorkingType.CONTRACT_PRICE.value,  # Làm việc dựa trên giá hợp đồng
            "priceMatch": None
            if price
            else OrderPriceMatch.OPPONENT.value,  # TODO: Đây là chọn giá trong queue để khớp nhanh? Nhưng để tối ưu hóa lợi nhuận, có thể chọn 1 giá đẹp hơn
            # "selfTradePreventionMode": "NONE",  # Không ngăn chặn giao dịch tự động
            # "goodTillDate": 1693207680000,  # Thời gian hủy lệnh cho lệnh GTD
            "newOrderRespType": "RESULT",  # Loại phản hồi của lệnh
            "priceProtect": False,  # TODO: Có nên dùng price protect để ensure giá không bị thay đổi quá nhanh làm trigger lệnh stop loss???
        }

        res = client.new_order(**order_data)

        self._logger.info("Success create stop loss order: {}".format(res))

        return OrderResponse(**res)

    def create_limit_order(
        self,
        client_order_id: str,
        symbol: str,
        side: OrderSide,
        qty: float,
        price: float = None,
        reduce_only: bool = False,
    ):
        self._logger.will("create TP order")
        client = get_um_client()

        order_data = {
            "newClientOrderId": client_order_id,
            "symbol": symbol,
            "side": side.value,  # Mua hoặc bán
            # "positionSide": OrderPositionSide.LONG.value,
            "type": OrderType.LIMIT.value,  # Loại lệnh TRAILING_STOP_MARKET
            "timeInForce": OrderTimeInForce.GTC.value,  # Loại thời gian hiệu lực GTD
            "quantity": qty,  # Số lượng
            "price": price,  # TODO: priceMatch
            # "stopPrice": stop_price,  # Giá dừng (Stop Price)
            # "closePosition": false,  # Không đóng tất cả vị trí
            # "workingType": OrderWorkingType.CONTRACT_PRICE.value,  # Làm việc dựa trên giá hợp đồng
            "priceMatch": None
            if price
            else OrderPriceMatch.OPPONENT.value,  # TODO: Đây là chọn giá trong queue để khớp nhanh? Nhưng để tối ưu hóa lợi nhuận, có thể chọn 1 giá đẹp hơn
            # "selfTradePreventionMode": "NONE",  # Không ngăn chặn giao dịch tự động
            # "goodTillDate": 1693207680000,  # Thời gian hủy lệnh cho lệnh GTD
            "newOrderRespType": "RESULT",  # Loại phản hồi của lệnh
            "priceProtect": False,
            "reduceOnly": reduce_only,
        }

        res = client.new_order(**order_data)

        return OrderResponse(**res)

    def create_mk_order(
        self,
        symbol: str,
        side: OrderSide,
        qty: float,
    ) -> OrderResponse:
        """
        TODO: FOR TESTING ONLY
        :param symbol:
        :param side:
        :param qty:
        """

        self._logger.will("create new order: {}".format(symbol))
        client = get_um_client()

        order_data = {
            "symbol": symbol,
            "side": side.value,  # Mua hoặc bán
            # "positionSide": OrderPositionSide.LONG.value,
            "type": OrderType.MARKET.value,  # Loại lệnh TRAILING_STOP_MARKET
            "quantity": qty,  # Số lượng
            # "closePosition": false,  # Không đóng tất cả vị trí
            # "selfTradePreventionMode": "NONE",  # Không ngăn chặn giao dịch tự động
            # "goodTillDate": 1693207680000,  # Thời gian hủy lệnh cho lệnh GTD
            "newOrderRespType": "RESULT",  # Loại phản hồi của lệnh
        }

        res = client.new_order(**order_data)

        order_info = OrderResponse(**res)

        self._logger.info("New order response: {}".format(order_info))

        return order_info

    def get_current_open_orders(self, symbol: str) -> List[OrderResponse]:
        self._logger.debug("Getting open orders")
        client = get_um_client()
        orders = client.get_orders(symbol=symbol)

        data = [OrderResponse(**order) for order in orders]
        self._logger.debug("Success fetched open orders: {}".format(data))

        return data
