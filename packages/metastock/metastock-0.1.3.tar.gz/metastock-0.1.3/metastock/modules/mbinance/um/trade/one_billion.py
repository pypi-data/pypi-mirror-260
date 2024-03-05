from typing import Callable

from dependency_injector.wiring import Provide
from reactivex.subject import BehaviorSubject
from rich.panel import Panel
from rich.text import Text

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.environment import env
from metastock.modules.core.util.r.handle_error import handle_error
from metastock.modules.core.util.r.schedule_one_thread import schedule_one_thread
from metastock.modules.mbinance.error.fatal_error import FatalError
from metastock.modules.mbinance.exchange.connector.base.api_account_connector_base import (
    ApiAccountConnectorBase,
)
from metastock.modules.mbinance.exchange.connector.base.api_data_connector_base import (
    ApiDataConnectorBase,
)
from metastock.modules.mbinance.um.api_schema.event.account_update_event import (
    AccountUpdateEvent,
)
from metastock.modules.mbinance.um.api_schema.event.order_update_event import (
    OrderTradeUpdateEvent,
)
from metastock.modules.mbinance.um.exchange.general.time.is_local_time_match_server import (
    is_local_time_match_server,
)
from metastock.modules.mbinance.um.r.actions.ac_001_market_data_update import (
    AC_001_MARKET_DATA_UPDATE,
)
from metastock.modules.mbinance.um.r.actions.ac_003_account_balance_update import (
    AC_003_ACCOUNT_UPDATE,
)
from metastock.modules.mbinance.um.r.actions.ac_004_get_account_balance import (
    AC_004_GET_ACCOUNT_BALANCE,
)
from metastock.modules.mbinance.um.r.actions.ac_008_order_trade_update import (
    AC_008_ORDER_TRADE_UPDATE,
)
from metastock.modules.mbinance.um.r.actions.order.position.ac_t01_get_position import (
    AC_T01_GET_POSITION,
)
from metastock.modules.mbinance.um.r.um_r_manager import UMRManager
from metastock.modules.mbinance.um.util.dump_kline import dump_kline
from metastock.modules.mbinance.um.value.um_value import UMValue
from metastock.modules.mbinance.value.common import TimeInterval


class OneBillion:
    def __init__(
        self,
        api_data_connector_factory: Callable[..., ApiDataConnectorBase],
        api_account_connector: ApiAccountConnectorBase = Provide[
            "mbinance.um.api_account_connector"
        ],
        r: UMRManager = Provide["mbinance.um.um_r_manager"],
        logger: AppLogger = Provide["core.logger"],
    ) -> None:
        self._r = r
        self._logger = logger
        self._api_data_connector_factory = api_data_connector_factory
        self._api_account_connector = api_account_connector

        self.__api_data_subscriber = {}
        self.__api_data_connectors: list[ApiDataConnectorBase] = []
        self.__user_data_subscriber = None

    def _validate_environment(self) -> None:
        self._logger.debug("Validating environment")
        if is_local_time_match_server() is False:
            raise FatalError("Local time not match with server")

        symbol = UMValue.SYMBOL()

        if symbol is None:
            raise FatalError("Missing SYMBOL environment variable")
        else:
            self._logger.console().print(
                Panel(
                    Text(
                        f"{symbol}",
                        justify="center",
                    ),
                    title="Symbol",
                )
            )

        self._logger.debug("OK validate environment")

    def start(self, pair: str):
        self._logger.info("Starting one billion trade for pair: {}".format(pair))

        # Validate environments
        self._validate_environment()

        # _______ get current account/position _______
        if env().get("TRADE") == "true":
            self._r.dispatch(AC_004_GET_ACCOUNT_BALANCE())
            self._r.dispatch(AC_T01_GET_POSITION())

        # _______ Api Account connector (user data: postion, order trade update) _______
        self._api_account_connector.initialize()
        self.__subscribe_user_data_ob(
            self._api_account_connector.get_api_user_data_ob()
        )

        # _______ Api Data connector (market data: kline) _______
        api_data_connector_30m = self._api_data_connector_factory(
            interval=TimeInterval.THIRTY_MINUTES.value
        )
        api_data_connector_30m.initialize()
        self.__api_data_connectors.append(api_data_connector_30m)
        self.__subscribe_market_data_ob(
            "api_data_connector_30m", api_data_connector_30m.get_api_market_data_ob()
        )

    def stop(self):
        self._logger.info("Stopping one billion trade")

        self._r.stop()
        self._logger.info("Stopped effects")

        for api_data_connector in self.__api_data_connectors:
            api_data_connector.stop()
        self._logger.info("Stopped api data connectors")

        for _, api_data_subscriber in self.__api_data_subscriber.items():
            api_data_subscriber.dispose()
        self._logger.info("Stopped api data subscribers")

        if self.__user_data_subscriber is not None:
            self.__user_data_subscriber.dispose()
        self._logger.info("Stopped user data subscriber")

    def __subscribe_market_data_ob(self, key: str, data_ob: BehaviorSubject):
        if self.__api_data_subscriber.get(key) is not None:
            return

        def __handle_data_update(data):
            if type(data) is dict:
                kline_data: dict = data.get("kline_data")

                kline = kline_data.get("kline")
                dump_kline(kline=kline)
                self._r.dispatch(AC_001_MARKET_DATA_UPDATE(kline_data))

        self.__api_data_subscriber[key] = data_ob.pipe(schedule_one_thread()).subscribe(
            on_next=__handle_data_update, on_error=handle_error
        )

    def __subscribe_user_data_ob(self, user_data_ob: BehaviorSubject):
        if self.__user_data_subscriber:
            return

        def __handle_data_update(data):
            if type(data) is AccountUpdateEvent:
                self._logger.info(
                    f"Dispatching [magenta u]'{AC_003_ACCOUNT_UPDATE.name}'[/magenta u]: {data}"
                )
                self._r.dispatch(AC_003_ACCOUNT_UPDATE(data))

            if type(data) is OrderTradeUpdateEvent:
                self._logger.info(
                    f"Dispatching [magenta u]'{AC_008_ORDER_TRADE_UPDATE.name}'[/magenta u]: {data}"
                )
                self._r.dispatch(AC_008_ORDER_TRADE_UPDATE(data))

        def __on_error(error):
            self._logger.exception(error)

        self.__user_data_subscriber = user_data_ob.pipe(
            schedule_one_thread()
        ).subscribe(on_next=__handle_data_update, on_error=__on_error)
