from dependency_injector.wiring import inject
from sqlalchemy import update
from sqlalchemy.orm import Session

from metastock.modules.core.db.postgres_manager import postgres_manager
from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.mbinance.um.db.models import HistoryDataFetcherState
from metastock.modules.mbinance.um.exchange.general.time.format_ms import format_ms


@inject
class FetcherStateResource:
    def __init__(self, logger: AppLogger):
        self._logger = logger

        self.__current_fetcher_state = {}

    def _refresh_fetcher_state(self, fetcher_type: str):
        with postgres_manager.get_session() as session:
            self.__current_fetcher_state[fetcher_type] = (
                session.query(HistoryDataFetcherState)
                .filter_by(type=fetcher_type)
                .first()
            )

    def get_fetcher_state(
        self, pair: str, interval: str, refresh: bool = False
    ) -> HistoryDataFetcherState:
        fetcher_type = self._get_fetcher_state_type(pair, interval)
        if self.__current_fetcher_state.get(fetcher_type) is None or refresh is True:
            self._refresh_fetcher_state(fetcher_type=fetcher_type)

        return self.__current_fetcher_state[fetcher_type]

    def _get_fetcher_state_type(self, pair: str, interval: str):
        return f"{pair}_{interval}"

    def update_fetcher_state(
        self,
        session: Session,
        pair: str,
        interval: str,
        start_time: int,
        end_time: int,
    ) -> None:
        fetcher_type = self._get_fetcher_state_type(pair, interval)
        current_state = self.get_fetcher_state(
            pair=pair, interval=interval, refresh=True
        )

        if current_state:
            session.execute(
                update(HistoryDataFetcherState)
                .where(HistoryDataFetcherState.id == current_state.id)
                .values(end_time=end_time)
            )
        else:
            session.add(
                HistoryDataFetcherState(
                    type=fetcher_type,
                    start_time=start_time,
                    end_time=end_time,
                    number_of_try=1,
                    last_error=None,
                )
            )

        self._logger.debug(
            f"Success update fetcher state for '{fetcher_type}' with last updated time {end_time}({format_ms(end_time)})"
        )
