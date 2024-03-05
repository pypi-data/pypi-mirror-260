from metastock.modules.core.db.postgres_manager import postgres_manager
from metastock.modules.core.util.app_error import AppError
from metastock.modules.core.util.registry import registry
from metastock.modules.mbinance.um.api_schema.response.candless_tick import (
    ContinuousContractKline,
)
from metastock.modules.mbinance.um.db.models import Candlestick
from metastock.modules.mbinance.um.exchange.general.time.format_ms import format_ms
from metastock.modules.mbinance.um.exchange.history.api.get_klines import get_klines
from metastock.modules.mbinance.um.exchange.history.fetch.fetcher_base import (
    FetcherBase,
)
from metastock.modules.mbinance.um.value.um_value import UMValue


class CandlestickFetcher(FetcherBase):
    __type__ = "candlestick"

    def _load_data(self, start_time: int, end_time: int = None):
        try:
            self.logger.info(
                f"Load Candlestick Data for Timeframe {start_time}({format_ms(start_time)}) to {end_time}({format_ms(end_time)}) - (current page {self._current_page})"
            )
            pair = UMValue.PAIR()
            candlesticks = get_klines(
                start_time=start_time, end_time=end_time, pair=pair
            )

            # Do phút hiện tại có thể chưa closed nên sẽ bỏ qua
            if len(candlesticks.data) <= 1:
                if self._current_page == 1:
                    self.logger.warning("No Candlesticks data")
                else:
                    self.logger.ok("Finished retrieving Candlesticks")

                return

            # save to db
            self._save_to_db(candlesticks)

            self._update_fetcher_state()

            self.logger.will("Load next page...")
            # time.sleep(1)
            # load next page
            self._load_data(
                start_time=self._get_last_update_time() + 1, end_time=end_time
            )
        except Exception as e:
            self.logger.exception(e)
            self._update_fetcher_state(error=e)

    def _save_to_db(self, candlesticks: ContinuousContractKline):
        self.logger.info("Saving Candlestick")
        session = postgres_manager.get_session()
        try:
            # chỉ save phút trước đó
            candlesticks.data = candlesticks.data[1:]
            self._last_update_time = candlesticks.data[0].open_time
            candlesticks_data = []
            for candlestick in candlesticks.data:
                if candlestick.open_time > self._last_update_time:
                    self._last_update_time = candlestick.open_time

                candlesticks_data.append(Candlestick.map_from_pydantic(candlestick))

            self.logger.will(f"insert {len(candlesticks_data)} Candlesticks Data")
            session.add_all(candlesticks_data)
            session.commit()

            self._current_page += 1
            self.logger.ok(
                f"Candlestick saved with last updated time {self._last_update_time}({format_ms(self._last_update_time)})"
            )
        except Exception as e:
            session.rollback()
            # self.logger.exception(e)

            raise AppError("Error saving Candlestick Data") from e
        finally:
            session.close()
