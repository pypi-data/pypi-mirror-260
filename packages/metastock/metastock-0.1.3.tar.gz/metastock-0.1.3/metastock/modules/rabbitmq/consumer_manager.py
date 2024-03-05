from typing import List, Type

from metastock.modules.rabbitmq.consumer import RabbitMQConsumer


class ConsumerManager:
    INSTANCE = None

    def __init__(self):
        self._CONSUMERS: list = []

    def get_consumers(self) -> list[RabbitMQConsumer]:
        return self._CONSUMERS

    def get_consumer(self, name: str) -> RabbitMQConsumer | None:
        return next((item for item in self.get_consumers() if item.get_name() == name), None)

    def add_consumer(self, consumers: list[RabbitMQConsumer]):
        self._CONSUMERS = self._CONSUMERS + consumers


def consumer_manager() -> ConsumerManager:
    if ConsumerManager.INSTANCE is None:
        ConsumerManager.INSTANCE = ConsumerManager()

    return ConsumerManager.INSTANCE
