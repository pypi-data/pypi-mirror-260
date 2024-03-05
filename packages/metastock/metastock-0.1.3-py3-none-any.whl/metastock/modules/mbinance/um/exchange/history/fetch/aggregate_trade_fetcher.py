from metastock.modules.core.db.postgres_manager import postgres_manager
from metastock.modules.core.util.app_error import AppError
from metastock.modules.core.util.registry import registry
from metastock.modules.mbinance.um.api_schema.response.aggregate_trade_list import (
    AggregateTradeList,
)
from metastock.modules.mbinance.um.db.models import BinanceTrade
from metastock.modules.mbinance.um.exchange.general.time.format_ms import format_ms
from metastock.modules.mbinance.um.exchange.history.api.get_aggregate_trade import (
    get_aggregate_trade,
)
from metastock.modules.mbinance.um.exchange.history.fetch.fetcher_base import (
    FetcherBase,
)
from metastock.modules.mbinance.um.value.um_value import UMValue


class AggregateTradeFetcher(FetcherBase):
    __type__ = "aggregate_trade"

    def _load_data(self, start_time: int, end_time: int = None):
        self.logger.info(
            f"Loading aggregate trades from server for page {self._current_page} from {format_ms(start_time)} to {format_ms(end_time)}"
        )
        symbol = UMValue.SYMBOL()
        res = get_aggregate_trade(
            start_time=start_time, end_time=end_time, symbol=symbol
        )

        if len(res.data) == 0:
            if self._current_page == 1:
                self.logger.warning("No aggregate trades found")
            else:
                self.logger.ok("Finished loading aggregate")

            return

        self._save_to_db(res)
        self._load_data(start_time=self._get_last_update_time() + 1, end_time=end_time)

    def _save_to_db(self, data: AggregateTradeList):
        self.logger.info(f"Saving aggregate trades to database")
        session = postgres_manager.get_session()
        try:
            self._last_update_time = data.data[0].T
            trade_data = []
            for binance_trade_data in data.data:
                if binance_trade_data.T > self._last_update_time:
                    self._last_update_time = binance_trade_data.T

                trade_data.append(BinanceTrade.map_from_pydantic(binance_trade_data))

            self.logger.will(f"insert {len(trade_data)} aggregate trades")
            session.add_all(trade_data)

            session.commit()
            self._current_page += 1
            self.logger.ok("Saved aggregate trades to database")
        except Exception as e:
            session.rollback()
            self.logger.exception(e)

            raise AppError("Error saving aggregate trades to database") from e
        finally:
            session.close()
