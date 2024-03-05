from dependency_injector import containers, providers

from metastock.modules.core.container import CoreContainer
from metastock.modules.mbinance.um.db.resources.fetcher_state_resource import (
    FetcherStateResource,
)
from metastock.modules.mbinance.um.exchange.connector.api_account_connector import (
    UMApiAccountConnector,
)
from metastock.modules.mbinance.um.exchange.connector.api_data_connector import (
    UMApiDataConnector,
)
from metastock.modules.mbinance.um.exchange.connector.api_order_connector import (
    UMApiOrderConnector,
)
from metastock.modules.mbinance.um.exchange.history.fetch.candlestick_fetcher_v2 import (
    CandlestickFetcherV2,
)
from metastock.modules.mbinance.um.exchange.um_socket_manager import UMSocketManager
from metastock.modules.mbinance.um.r.effects.account.get_account_balance import (
    GetAccountBalanceEffect,
)
from metastock.modules.mbinance.um.r.effects.compare_server_time import (
    CompareServerTimeEffect,
)
from metastock.modules.mbinance.um.r.effects.history.candlestick_fetcher_effects import (
    CandlestickLoadNextPageEffect,
    CandlestickLoadPageEffect,
    CandlestickLoadPageSuccessEffect,
)
from metastock.modules.mbinance.um.r.effects.market.receive_kline import (
    ReceiveKlineEffect,
)
from metastock.modules.mbinance.um.r.effects.trade.cancel_tp_order_when_close_pos import (
    CancelTPOrderWhenClosePosEffect,
)
from metastock.modules.mbinance.um.r.effects.trade.check_create_tp_order import (
    CheckCreateTPOrderEffect,
)
from metastock.modules.mbinance.um.r.effects.trade.create_tp_order import (
    CreateTPOrderEffect,
)
from metastock.modules.mbinance.um.r.effects.trade.get_position import GetPositionEffect
from metastock.modules.mbinance.um.r.effects.trade.monitoring.position_monitoring import (
    PositionMonitoringEffect,
)
from metastock.modules.mbinance.um.r.um_r_manager import UMRManager
from metastock.modules.mbinance.um.trade.one_billion import OneBillion
from metastock.modules.mbinance.um.trade.strategy.history_test.queue.consumer.msell_v1_consumer import (
    MSellV1Consumer,
)

_CONSUMERS_ = [MSellV1Consumer]


class UmContainer(containers.DeclarativeContainer):
    core: CoreContainer = providers.DependenciesContainer()
    logger = core.logger

    # Resources
    fetcher_state_resource = providers.ThreadSafeSingleton(
        FetcherStateResource, logger=logger
    )

    # exchange connector
    um_socket_manager = providers.ThreadSafeSingleton(UMSocketManager, logger=logger)

    api_account_connector = providers.ThreadSafeSingleton(
        UMApiAccountConnector, um_socket_manager=um_socket_manager, logger=logger
    )
    api_data_connector_factory = providers.Factory(
        UMApiDataConnector, logger=logger, um_socket_manager=um_socket_manager
    )
    api_order_connector = providers.ThreadSafeSingleton(
        UMApiOrderConnector, logger=logger
    )

    # register R and it's effects
    um_r_manager = providers.ThreadSafeSingleton(
        UMRManager,
        logger=logger,
        effects=providers.List(
            providers.ThreadSafeSingleton(CompareServerTimeEffect),
            providers.ThreadSafeSingleton(
                GetAccountBalanceEffect,
                logger=logger,
                api_account_connector=api_account_connector,
            ),
            providers.ThreadSafeSingleton(ReceiveKlineEffect, logger=logger),
            providers.ThreadSafeSingleton(CheckCreateTPOrderEffect, logger=logger),
            providers.ThreadSafeSingleton(
                CreateTPOrderEffect,
                logger=logger,
                api_order_connector=api_order_connector,
            ),
            providers.ThreadSafeSingleton(
                GetPositionEffect,
                logger=logger,
                api_account_connector=api_account_connector,
            ),
            providers.ThreadSafeSingleton(
                PositionMonitoringEffect,
                logger=logger,
            ),
            providers.ThreadSafeSingleton(
                CancelTPOrderWhenClosePosEffect,
                logger=logger,
                api_order_connector=api_order_connector,
            ),
            # HISTORY FETCHER EFFECTS
            providers.ThreadSafeSingleton(
                CandlestickLoadPageEffect,
                logger=logger,
            ),
            providers.ThreadSafeSingleton(
                CandlestickLoadPageSuccessEffect,
                fetcher_state_resource=fetcher_state_resource,
                logger=logger,
            ),
            providers.ThreadSafeSingleton(
                CandlestickLoadNextPageEffect,
            ),
        ),
    )

    # trade
    one_billion = providers.ThreadSafeSingleton(
        OneBillion, api_data_connector_factory=api_data_connector_factory.provider
    )

    # Fetcher
    candlestick_fetcher_v2 = providers.ThreadSafeSingleton(
        CandlestickFetcherV2,
        logger=logger,
        r=um_r_manager,
        fetcher_state_resource=fetcher_state_resource,
    )

    # Consumers
    for consumer in _CONSUMERS_:
        providers.Singleton(consumer)
