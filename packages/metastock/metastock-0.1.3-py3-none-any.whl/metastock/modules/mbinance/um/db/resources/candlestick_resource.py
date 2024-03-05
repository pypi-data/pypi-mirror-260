import arrow
import pandas as pd
from sqlalchemy import and_

from metastock.modules.core.db.postgres_manager import postgres_manager
from metastock.modules.mbinance.um.db.models import Candlestick
from metastock.modules.mbinance.value.common import CommonValue, TimeInterval


def get_candlestick_history_df(
    symbol: str, start: int, end: int, interval: TimeInterval | str
) -> pd.DataFrame:
    with postgres_manager.get_session_factory().begin() as session:
        data = (
            session.query(Candlestick)
            .filter(
                and_(
                    Candlestick.symbol == symbol,
                    Candlestick.interval == interval,
                    Candlestick.open_time <= end,
                    Candlestick.open_time >= start,
                )
            )
            .order_by(Candlestick.open_time.desc())
        )

        df = pd.read_sql_query(sql=data.statement, con=postgres_manager.get_engine())
        df["open_time"] = df["open_time"].apply(
            lambda x: arrow.get(x / 1000).to(CommonValue.TIME_ZONE).datetime
        )
        df.set_index("open_time", inplace=True)

        return df
