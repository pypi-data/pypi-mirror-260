import pika
from pika.adapters.blocking_connection import BlockingChannel

from metastock.modules.core.logging.logger import Logger


class RabbitMQPublisher:
    def __init__(self, connection: pika.BlockingConnection):
        self.connection = connection

        self.__is_declared_exchange = False
        self.__channel = None

    def _get_chanel(self) -> BlockingChannel:
        if self.__channel is None:
            self.__channel = self.connection.channel()

        return self.__channel

    def _exchange_declare(self, exchange, exchange_type="topic"):
        if not self.__is_declared_exchange:
            self._get_chanel().exchange_declare(
                exchange=exchange,
                exchange_type=exchange_type,
                durable=True,
                passive=False,
            )
            self.__is_declared_exchange = True

    def publish(self, exchange, routing_key, message):
        self._exchange_declare(exchange=exchange)
        self._get_chanel().basic_publish(
            exchange=exchange, routing_key=routing_key, body=message
        )
        Logger().info(
            f"Message '{message}' published to exchange '{exchange}' with routing_key '{routing_key}'."
        )
