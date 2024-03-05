from dependency_injector.wiring import Provide

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.environment import env
from metastock.modules.mbinance.error.fatal_error import FatalError
from metastock.modules.mbinance.exchange.connector.base.api_account_connector_base import (
    ApiAccountConnectorBase,
)
from metastock.modules.mbinance.um.api_schema.event.account_update_event import (
    AccountUpdateEvent,
)
from metastock.modules.mbinance.um.api_schema.event.order_update_event import (
    OrderTradeUpdateEvent,
)
from metastock.modules.mbinance.um.api_schema.response.account_balance_v2 import (
    AccountBalanceResponse,
)
from metastock.modules.mbinance.um.api_schema.response.position_info import (
    PositionInfoResponse,
)
from metastock.modules.mbinance.um.exchange.um_socket_manager import UMSocketManager
from metastock.modules.mbinance.um.util.get_client import get_um_client
from metastock.modules.mbinance.um.value.um_event_type import UMEventType


class UMApiAccountConnector(ApiAccountConnectorBase):
    def __init__(
        self,
        um_socket_manager: UMSocketManager = Provide["mbinance.um.um_socket_manager"],
        logger: AppLogger = Provide["core.logger"],
    ):
        self._um_socket_manager = um_socket_manager
        super().__init__(logger)

        self.__initialized = False

    def initialize(self):
        if self.__initialized:
            return

        if env().get("TRADE") == "true":
            self._um_socket_manager.register_handler(
                UMEventType.ACCOUNT_UPDATE.value, self._handle_account_update
            )
            self._um_socket_manager.register_handler(
                UMEventType.ORDER_TRADE_UPDATE.value, self._handle_order_trade_update
            )

            socket = self._um_socket_manager.get_socket()
            client = get_um_client()
            response = client.new_listen_key()

            self._logger.debug("Listen key : {}".format(response["listenKey"]))
            socket.user_data(
                listen_key=response["listenKey"],
            )

        self.__initialized = True

    def _handle_account_update(self, event_object):
        if event_object.get("e") != UMEventType.ACCOUNT_UPDATE.value:
            return

        self._logger.debug("Received account update event: {}".format(event_object))
        try:
            account_update_event = AccountUpdateEvent(**event_object)
            self._logger.debug(
                "Success validate account update event: {}".format(account_update_event)
            )
            self._api_user_data_ob.on_next(account_update_event)
        except Exception as err:
            self._logger.error("Error parsing account update event: {}".format(err))

            raise FatalError("Error parsing account update event")

    def _handle_order_trade_update(self, event_object):
        if event_object.get("e") != UMEventType.ORDER_TRADE_UPDATE.value:
            return

        self._logger.debug("Received order trade update event: {}".format(event_object))
        try:
            order_update_event = OrderTradeUpdateEvent(**event_object)
            self._logger.debug(
                "Success validate order trade event: {}".format(order_update_event)
            )

            self._api_user_data_ob.on_next(order_update_event)
        except Exception as err:
            self._logger.error("Error parsing order trade update event: {}".format(err))

            raise FatalError("Error parsing order trade update event")

    def get_positions(self):
        client = get_um_client()

        positions = client.get_position_risk()

        return PositionInfoResponse(data=positions)

    def get_account_balance(self):
        client = get_um_client()

        balance = client.balance()

        return AccountBalanceResponse(data=balance)

    def stop(self):
        self._um_socket_manager.stop()
