import abc

from metastock.modules.mbinance.exchange.connector.base.connector_base import (
    ConnectorBase,
)
from metastock.modules.mbinance.um.api_schema.response.order import OrderResponse
from metastock.modules.mbinance.um.value.um_order_type import OrderSide


class ApiOrderConnectorBase(ConnectorBase):
    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def create_sl_order(
        self,
        client_order_id: str,
        symbol: str,
        side: OrderSide,
        stop_price: float,
        qty: float,
        price: float = None,
    ):
        pass

    @abc.abstractmethod
    def create_limit_order(
        self,
        client_order_id: str,
        symbol: str,
        side: OrderSide,
        qty: float,
        price: float = None,
        reduce_only: bool = False,
    ):
        pass

    @abc.abstractmethod
    def create_mk_order(
        self,
        symbol: str,
        side: OrderSide,
        qty: float,
    ) -> OrderResponse:
        pass
