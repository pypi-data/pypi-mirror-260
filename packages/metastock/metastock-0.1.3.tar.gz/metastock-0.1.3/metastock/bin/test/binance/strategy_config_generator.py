import pickle
from itertools import product

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.environment import config_env
from metastock.modules.mbinance.um.trade.strategy.config.sell_strategy_v1_config import (
    SellStrategyV1Config,
)
from metastock.modules.mbinance.um.value.um_queue_value import UMQueueValue
from metastock.modules.mbinance.value.common import TimeInterval
from metastock.modules.rabbitmq.connection_manager import rabbitmq_manager
from metastock.modules.rabbitmq.publisher import RabbitMQPublisher

config_env("BN")
rabbitmq_manager().initialize()
publisher = RabbitMQPublisher(
    rabbitmq_manager().get_connection().get_rabbit_connection()
)

SYMBOL = "BTCUSDT"
start_time = "2023-11-01 00:00:00"
end_time = "2024-03-01 00:00:00"


def _generate_list(start: float, end: float, step: float) -> list:
    float_list = []
    current = start
    while current <= end:
        float_list.append(current)
        current = round(current + step, 2)

    return float_list


def generate_msell_v1(interval: TimeInterval = TimeInterval.THIRTY_MINUTES.value):
    """
    Generate for msell v1 strategy
    :param interval:
    :return:
    """
    # default_strategy_config = SellStrategyV1Config(
    #     tp=0.5,
    #     sl=0.5,
    #     wt_diff_check=[4, 2],
    #     wt1_check=[3],
    #     hull_diff_check=[20, 20],
    #     hull_check=[-20, 20],
    #     is_check_hull=True,
    # )

    def _publish_strategy(
        tp,
        sl,
        wt_diff_check_0,
        wt_diff_check_1,
        wt_check_0,
        hull_diff_check_0,
        hull_diff_check_1,
    ):
        strategy_config = SellStrategyV1Config(
            tp=tp,
            sl=sl,
            wt_diff_check=[wt_diff_check_0, wt_diff_check_1],
            wt1_check=[wt_check_0],
            hull_diff_check=[hull_diff_check_0, hull_diff_check_1],
            hull_check=[-20, 20],
            is_check_hull=True,
        )
        serialized_object = pickle.dumps(
            {
                "symbol": SYMBOL,
                "start_time": start_time,
                "end_time": end_time,
                "interval": interval,
                "strategy_config": strategy_config,
            }
        )
        Logger().info(
            f"Publish tp {tp} | sl {sl} | wt_diff_check_0 {wt_diff_check_0} | wt_diff_check_1 {wt_diff_check_1} | wt_check_0 {wt_check_0}"
        )
        publisher.publish(
            exchange=UMQueueValue.MSELL_EXCHANGE,
            routing_key=UMQueueValue.MSELL_V1_ROUTING,
            message=serialized_object,
        )

    for combinations in product(
        [0.2],  # tp
        [0.1],  # sl
        _generate_list(2, 2, 1),  # Độ chênh lệch giữa 2 wt_diff(slope)
        _generate_list(4, 4, 1),  # Giá trị hiện tại MAX của wt_diff
        _generate_list(4, 4, 1),  # Slope của wt1
        _generate_list(15, 30, 1),  # Max của hull
        _generate_list(15, 30, 1),  # Max weight của hull so với đỉnh
    ):
        _publish_strategy(*combinations)


def publish_strategy():
    strategy_config = SellStrategyV1Config(
        tp=0.2,
        sl=0.1,
        wt_diff_check=[2, 4],
        wt1_check=[4],
        hull_diff_check=[20, 20],
        hull_check=[-20, 20],
        is_check_hull=True,
        is_check_hull_condition_2=False,
    )
    serialized_object = pickle.dumps(
        {
            "symbol": SYMBOL,
            "start_time": start_time,
            "end_time": end_time,
            "interval": TimeInterval.THIRTY_MINUTES.value,
            "strategy_config": strategy_config,
        }
    )
    publisher.publish(
        exchange=UMQueueValue.MSELL_EXCHANGE,
        routing_key=UMQueueValue.MSELL_V1_ROUTING,
        message=serialized_object,
    )


# publish_strategy()
generate_msell_v1(interval=TimeInterval.THIRTY_MINUTES.value)
