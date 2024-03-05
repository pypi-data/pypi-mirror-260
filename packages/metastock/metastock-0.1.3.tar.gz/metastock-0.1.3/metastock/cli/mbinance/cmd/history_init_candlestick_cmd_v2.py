from dependency_injector.wiring import inject, Provide

from metastock.modules.core.db.postgres_manager import postgres_manager
from metastock.modules.core.util.exit_event import hold
from metastock.modules.mbinance.um.exchange.history.fetch.candlestick_fetcher_v2 import (
    CandlestickFetcherV2,
)


@inject
def history_init_candlestick_cmd_v2(
    pair: str,
    interval: str,
    candlestick_fetcher_v2: CandlestickFetcherV2 = Provide[
        "mbinance.um.candlestick_fetcher_v2"
    ],
):
    postgres_manager.initialize()
    candlestick_fetcher_v2.fetch(pair=pair, interval=interval)

    hold()
