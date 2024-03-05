import inspect
import json
from typing import Callable

from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.mbinance.util.is_testnet import is_testnet
from metastock.modules.mbinance.value.common import CommonValue


class UMSocketManager:
    def __init__(self, logger: AppLogger):
        self._logger = logger

        self.__initialized = False
        self.__socket = None
        self.__handlers = {}
        self.__closed = False

    def initialize(self):
        if self.__initialized:
            return

        if self.__socket is None:
            self.__socket = (
                UMFuturesWebsocketClient(
                    on_message=self._socket_message_handler,
                    stream_url=CommonValue.API_TESTNET_STREAM_URL,
                )
                if is_testnet()
                else UMFuturesWebsocketClient(
                    on_message=self._socket_message_handler,
                )
            )

        self.__initialized = True

    def get_socket(self) -> UMFuturesWebsocketClient:
        if self.__socket is None:
            self.initialize()

        return self.__socket

    def _socket_message_handler(self, _, message):
        self._logger.debug("Received socket message: {}".format(message))

        try:
            event_object: dict = json.loads(message)
        except Exception as e:
            self._logger.error("Error parsing event stream data: {}".format(e))
            return

        for key, handler in self.__handlers.items():
            try:
                if isinstance(handler, Callable):
                    handler(event_object)
            except Exception as e:
                self._logger.error(
                    f"Error {e} when processing event handler with key: {key}",
                    exc_info=True,
                )

    def register_handler(self, event_name: str, handler: Callable):
        if self.__handlers.get(event_name):
            self._logger.warning(
                "Already registered handler for event {}".format(event_name)
            )

        self.__handlers[event_name] = handler

        return self

    def stop(self):
        if self.__closed:
            return
        self.__socket.stop()
        self.__closed = True
