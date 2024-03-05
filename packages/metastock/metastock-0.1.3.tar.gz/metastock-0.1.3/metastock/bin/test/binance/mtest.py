from metastock.modules.core.db.postgres_manager import postgres_manager
from metastock.modules.core.util.environment import config_env
from metastock.modules.core.util.registry import registry
from metastock.modules.mbinance.um.trade.strategy.config.sell_strategy_v1_config import (
    SellStrategyV1Config,
)
from metastock.modules.mbinance.um.trade.strategy.history_test.history_sell_test import (
    HistorySellTest,
)
from metastock.modules.mbinance.um.value.um_value import UMValue
from metastock.modules.mbinance.value.common import TimeInterval

config_env("BN")
postgres_manager.initialize()

# session = postgres_manager.get_session()
# datetime_string = "2024-02-16 20:51:00"
# max_open_time = int(
#     arrow.get(datetime_string, "YYYY-MM-DD HH:mm:ss")
#     .replace(tzinfo="Asia/Bangkok")
#     .timestamp()
#     * 1000
# )
# data = (
#     session.query(Candlestick)
#     .filter(and_(Candlestick.open_time <= max_open_time))
#     .order_by(Candlestick.open_time.desc())
#     .limit(120)
# )
#
# df = pd.read_sql_query(sql=data.statement, con=postgres_manager.get_engine())
# df["open_time"] = df["open_time"].apply(
#     lambda x: arrow.get(x / 1000).to(CommonValue.TIME_ZONE).datetime
# )
# df.set_index("open_time", inplace=True)
#
# mbuy_v1 = MBuyV1Strategy(kline=df)
# mbuy_v1.run(df)


# history_test = HistoryBuyTest(start_time="2024-02-16 20:11:00")
# history_test.start()


# ____________________________________________________________________________________________________
# registry.set_data(UMValue.PAIR_KEY, "ARBUSDT")
UMValue.set_PAIR("BTCUSDT")
# TODO: test time
start_time = "2023-03-04 00:00:00"
end_time = "2024-03-04 14:00:00"
# end_time = arrow.utcnow().replace(tzinfo="Asia/Bangkok").format("YYYY-MM-DD HH:mm:SS")

# start_time = "2024-02-23 19:30:00"
# end_time = None


btcusdt_30_strategy_config = SellStrategyV1Config(
    tp=0.2,
    sl=0.2,
    wt_diff_check=[2, 6],
    wt1_check=[4],
    hull_diff_check=[20, 20],
    hull_check=[-20, 20],
    is_check_hull=True,
    max_adj_price=0.1,
)

history_test = HistorySellTest(
    strategy_config=btcusdt_30_strategy_config,
    start_time=start_time,
    interval=TimeInterval.THIRTY_MINUTES.value,
    end_time=end_time,
).start()
