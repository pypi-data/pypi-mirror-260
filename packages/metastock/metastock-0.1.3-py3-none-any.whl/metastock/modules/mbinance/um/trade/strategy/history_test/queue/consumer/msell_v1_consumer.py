import pickle
from typing import Any

from dependency_injector.wiring import Provide
from pika.channel import Channel
from pydantic import BaseModel

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.mbinance.um.trade.strategy.history_test.history_sell_test import (
    HistorySellTest,
)
from metastock.modules.mbinance.um.value.um_queue_value import UMQueueValue
from metastock.modules.mbinance.um.value.um_value import UMValue
from metastock.modules.rabbitmq.consumer import RabbitMQConsumer


class MessageSchema(BaseModel):
    symbol: str
    interval: str
    start_time: str
    end_time: str
    strategy_config: Any


class MSellV1Consumer(RabbitMQConsumer):
    name = "msell_v1_consumer"

    def __init__(self, logger: AppLogger = Provide["core.logger"]):
        super().__init__(
            exchange=UMQueueValue.MSELL_EXCHANGE,
            queue=f"{UMQueueValue.MSELL_V1_QUEUE}",
            routing_key=f"{UMQueueValue.MSELL_V1_ROUTING}",
        )
        self._logger = logger

    def get_name(self):
        return MSellV1Consumer.name

    def handle_message(self, ch: Channel, method, properties, body):
        try:
            data = pickle.loads(body)
            self._logger.info(f"Received message: {data}")
            data = MessageSchema(**data)
            symbol = data.symbol
            interval = data.interval
            start_time = data.start_time
            end_time = data.end_time
            strategy_config = data.strategy_config

            UMValue.set_PAIR(symbol)

            HistorySellTest(
                strategy_config=strategy_config,
                start_time=start_time,
                interval=interval,
                end_time=end_time,
            ).start()

            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            self._logger.info("Message acknowledged.")
        except Exception as e:
            self._logger.error("An error occurred: %s", e, exc_info=True)

            # Negative Acknowledge the message
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
