from dependency_injector.wiring import Provide

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.registry import registry
from metastock.modules.mbinance.um.db.resources.fetcher_state_resource import (
    FetcherStateResource,
)
from metastock.modules.mbinance.um.r.actions.history.candlestick_load_page_action import (
    CANDLESTICK_LOAD_PAGE_ACTION,
)
from metastock.modules.mbinance.um.r.um_r_manager import UMRManager
from metastock.modules.mbinance.um.value.um_fetcher_value import UMFetcherValue
from metastock.modules.mbinance.value.common import CommonValue


class CandlestickFetcherV2:
    def __init__(
        self,
        fetcher_state_resource: FetcherStateResource = Provide[
            "mbinance.um.fetcher_state_resource"
        ],
        logger: AppLogger = Provide["core.logger"],
        r: UMRManager = Provide["mbinance.um.um_r_manager"],
    ):
        self._logger = logger
        self._r = r
        self._fetcher_state_resource = fetcher_state_resource

    def fetch(
        self,
        pair: str,
        interval: str,
    ):
        self._logger.info(
            f"Start fetching candlestick for pair: {pair} and interval: {interval}"
        )
        start_time: int = int(CommonValue.HISTORICAL_START_TIME)
        end_time = None

        current_state = self._fetcher_state_resource.get_fetcher_state(
            pair=pair, interval=interval
        )

        if current_state is not None:
            start_time = int(current_state.end_time)

        registry.set_data(f"{UMFetcherValue.CANDLESTICK_TYPE}_pair", pair)
        registry.set_data(f"{UMFetcherValue.CANDLESTICK_TYPE}_interval", interval)
        registry.set_data(f"{UMFetcherValue.CANDLESTICK_TYPE}_start_time", start_time)
        registry.set_data(f"{UMFetcherValue.CANDLESTICK_TYPE}_end_time", end_time)

        self._r.dispatch(
            CANDLESTICK_LOAD_PAGE_ACTION(
                {
                    "pair": pair,
                    "start_time": start_time,
                    "end_time": end_time,
                    "interval": interval,
                }
            )
        )
