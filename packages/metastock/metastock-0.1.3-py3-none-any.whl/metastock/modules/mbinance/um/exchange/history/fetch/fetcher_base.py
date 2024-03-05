from abc import ABC, abstractmethod

from sqlalchemy import update

from metastock.modules.core.db.postgres_manager import postgres_manager
from metastock.modules.core.logging.logger import AppLogger, Logger
from metastock.modules.core.util.app_error import AppError
from metastock.modules.mbinance.um.db.models import HistoryDataFetcherState
from metastock.modules.mbinance.um.exchange.general.time.format_ms import format_ms
from metastock.modules.mbinance.value.common import CommonValue


class FetcherBase(ABC):
    __type__ = None

    def __init__(
        self,
        start_time: int = CommonValue.HISTORICAL_START_TIME,
        end_time: int = None,
        logger: AppLogger = None,
    ):
        self.end_time = end_time
        self.start_time = start_time
        self.logger = logger or Logger()

        self._current_page = 1
        self._last_update_time = None
        self._current_fetcher_state = None

    def _refresh_fetcher_state(self):
        with postgres_manager.get_session() as session:
            self._current_fetcher_state = (
                session.query(HistoryDataFetcherState)
                .filter_by(type=self.__type__)
                .first()
            )

    def _get_fetcher_state(self, refresh: bool = False) -> HistoryDataFetcherState:
        if self._current_fetcher_state is None or refresh is True:
            self._refresh_fetcher_state()

        return self._current_fetcher_state

    def _get_last_update_time(self) -> int:
        return self._last_update_time

    def _check_current_state_valid_time(self):
        self.logger.info("Checking current history date state is valid time")

        current_state = self._get_fetcher_state(refresh=True)
        self.logger.info(f"Current fetcher history current state {current_state}")

        if current_state:
            if current_state.start_time != self.start_time:
                raise AppError(
                    "Current state has different start time. Please consider to truncate data before fetching"
                )

    def fetch(self) -> None:
        self.logger.info(
            f"Start fetching history data from start time: {self.start_time} end time: {self.end_time}"
        )
        self._check_current_state_valid_time()

        current_state = self._get_fetcher_state()

        if current_state:
            self.logger.will(
                f"fetch data from LAST state with end time {current_state.end_time}"
            )
            if self.end_time is not None:
                if current_state.end_time < self.end_time:
                    self._load_data(
                        start_time=current_state.end_time + 1, end_time=self.end_time
                    )
                else:
                    self.logger.info(
                        "Skip fetch data due to current state end time is greater than the expected end time."
                    )

                    return
            else:
                self._load_data(start_time=current_state.end_time + 1)
        else:
            self.logger.will("fetch data from BEGINNING")
            self._load_data(start_time=self.start_time, end_time=self.end_time)

    def _update_fetcher_state(self, error: Exception = None) -> None:
        with postgres_manager.get_session_factory().begin() as session:
            current_state = self._get_fetcher_state()

            if error is not None:
                self.logger.info(f"Update ERROR fetcher state for '{self.__type__}'")
                if current_state:
                    current_state.last_error = str(error)
                    current_state.number_of_try += 1
                else:
                    session.add(
                        HistoryDataFetcherState(
                            type=self.__type__,
                            start_time=self.start_time,
                            end_time=None,
                            number_of_try=1,
                            last_error=str(error),
                        )
                    )
            else:
                self.logger.info(
                    f"Update SUCCESS fetcher state for '{self.__type__}' with last updated time {self._get_last_update_time()}({format_ms(self._get_last_update_time())})"
                )
                if current_state:
                    session.execute(
                        update(HistoryDataFetcherState)
                        .where(HistoryDataFetcherState.id == current_state.id)
                        .values(end_time=self._get_last_update_time())
                    )
                else:
                    session.add(
                        HistoryDataFetcherState(
                            type=self.__type__,
                            start_time=self.start_time,
                            end_time=self._get_last_update_time(),
                            number_of_try=1,
                            last_error=None,
                        )
                    )

    @abstractmethod
    def _load_data(self, start_time: int, end_time: int = None) -> None:
        pass
