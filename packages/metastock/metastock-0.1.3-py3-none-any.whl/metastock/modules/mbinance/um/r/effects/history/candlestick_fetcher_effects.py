from typing import List

from reactivex import compose, operators as ops

from metastock.modules.core.db.postgres_manager import postgres_manager
from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.app_error import AppError
from metastock.modules.core.util.exit_event import exit_application
from metastock.modules.core.util.r.action import Action
from metastock.modules.core.util.r.effect_base import EffectBase
from metastock.modules.core.util.r.rx_common import of_type
from metastock.modules.core.util.registry import registry
from metastock.modules.mbinance.um.api_schema.response.candless_tick import (
    Candlestick,
)
from metastock.modules.mbinance.um.db.models import Candlestick as CandlestickModel
from metastock.modules.mbinance.um.db.resources.fetcher_state_resource import (
    FetcherStateResource,
)
from metastock.modules.mbinance.um.exchange.general.time.format_ms import format_ms
from metastock.modules.mbinance.um.exchange.history.api.get_klines import get_klines
from metastock.modules.mbinance.um.r.actions.history.candlestick_fulfilled_action import (
    CANDLESTICK_FULFILLED_ACTION,
)
from metastock.modules.mbinance.um.r.actions.history.candlestick_load_page_action import (
    CANDLESTICK_LOAD_PAGE_ACTION,
)
from metastock.modules.mbinance.um.r.actions.history.candlestick_load_page_error_action import (
    CANDLESTICK_LOAD_PAGE_ERROR_ACTION,
)
from metastock.modules.mbinance.um.r.actions.history.candlestick_load_page_success_action import (
    CANDLESTICK_LOAD_PAGE_SUCCESS_ACTION,
)
from metastock.modules.mbinance.um.r.actions.history.candlestick_save_page_error_action import (
    CANDLESTICK_SAVE_PAGE_ERROR_ACTION,
)
from metastock.modules.mbinance.um.r.actions.history.candlestick_save_page_success_action import (
    CANDLESTICK_SAVE_PAGE_SUCCESS_ACTION,
)
from metastock.modules.mbinance.um.value.um_fetcher_value import UMFetcherValue
from metastock.modules.mbinance.value.common import TimeInterval


class CandlestickLoadPageEffect(EffectBase):
    def __init__(self, logger: AppLogger):
        self._logger = logger

    def effect(self, r):
        def __load_page(action: Action):
            pair: str = action.payload.get("pair")
            start_time: int = action.payload.get("start_time")
            end_time: int = action.payload.get("end_time")
            interval: TimeInterval = action.payload.get("interval")
            try:
                self._logger.info(
                    f"Loading Candlestick Data for pair {pair} with interval {interval} in timeframe {start_time}({format_ms(start_time)}) -> {end_time}({format_ms(end_time)})"
                )
                kline = get_klines(
                    start_time=start_time,
                    end_time=end_time,
                    pair=pair,
                    time_interval=interval,
                )

                # Do phút hiện tại có thể chưa closed nên sẽ bỏ qua
                if len(kline.data) <= 1:
                    self._logger.info(f"No data available")
                    exit_application()
                    return CANDLESTICK_FULFILLED_ACTION()
                else:
                    self._logger.info(f"Success load Candlestick Data")
                    return CANDLESTICK_LOAD_PAGE_SUCCESS_ACTION(
                        {"candlesticks": kline.data}
                    )
            except Exception as e:
                self._logger.exception(e)
                return CANDLESTICK_LOAD_PAGE_ERROR_ACTION(e)

        return compose(
            of_type(CANDLESTICK_LOAD_PAGE_ACTION),
            ops.map(__load_page),
        )


class CandlestickLoadPageSuccessEffect(EffectBase):
    def __init__(self, fetcher_state_resource: FetcherStateResource, logger: AppLogger):
        self._logger = logger
        self._fetcher_state_resource = fetcher_state_resource

    def effect(self, r):
        def __save_to_db(
            pair: str, interval: str, start_time: int, candlesticks: List[Candlestick]
        ):
            session = postgres_manager.get_session()
            try:
                # chỉ save những phút trước đó (remove current minute)
                candlesticks = candlesticks[1:]
                last_update_time = candlesticks[0].open_time
                candlesticks_data = []
                for candlestick in candlesticks:
                    # thuc ra khong can, chi la dam bao last_update_time la max open_time
                    if candlestick.open_time > last_update_time:
                        last_update_time = candlestick.open_time

                    candlesticks_data.append(
                        CandlestickModel.map_from_pydantic(
                            symbol=pair, interval=interval, candlestick_data=candlestick
                        )
                    )

                session.add_all(candlesticks_data)

                self._fetcher_state_resource.update_fetcher_state(
                    session=session,
                    start_time=start_time,
                    end_time=last_update_time,
                    pair=pair,
                    interval=interval,
                )

                session.commit()

                self._logger.info(
                    f"Success save {len(candlesticks_data)} candlesticks to database"
                )

                return last_update_time
            except Exception as e:
                session.rollback()
                raise AppError("Error saving Candlestick Data") from e
            finally:
                session.close()

        def __when_load_page_success(action: Action):
            candlesticks = action.payload.get("candlesticks")
            try:
                last_update_time = __save_to_db(
                    candlesticks=candlesticks,
                    # Do khong muon luu vao state nen se luu vao registry
                    pair=registry.get_data(f"{UMFetcherValue.CANDLESTICK_TYPE}_pair"),
                    interval=registry.get_data(
                        f"{UMFetcherValue.CANDLESTICK_TYPE}_interval"
                    ),
                    start_time=registry.get_data(
                        f"{UMFetcherValue.CANDLESTICK_TYPE}_start_time"
                    ),
                )

                return CANDLESTICK_SAVE_PAGE_SUCCESS_ACTION(
                    {"last_update_time": last_update_time}
                )
            except Exception as e:
                self._logger.exception(e)
                return CANDLESTICK_SAVE_PAGE_ERROR_ACTION()

        return compose(
            of_type(CANDLESTICK_LOAD_PAGE_SUCCESS_ACTION),
            ops.map(__when_load_page_success),
        )


class CandlestickLoadNextPageEffect(EffectBase):
    def effect(self, r):
        def __map_to_load_page(action: Action):
            last_update_time = action.payload.get("last_update_time")
            return CANDLESTICK_LOAD_PAGE_ACTION(
                {
                    "pair": registry.get_data(
                        f"{UMFetcherValue.CANDLESTICK_TYPE}_pair"
                    ),
                    "interval": registry.get_data(
                        f"{UMFetcherValue.CANDLESTICK_TYPE}_interval"
                    ),
                    "start_time": last_update_time + 1,
                    "end_time": registry.get_data(
                        f"{UMFetcherValue.CANDLESTICK_TYPE}_end_time"
                    ),
                }
            )

        return compose(
            of_type(CANDLESTICK_SAVE_PAGE_SUCCESS_ACTION),
            ops.map(__map_to_load_page),
        )
