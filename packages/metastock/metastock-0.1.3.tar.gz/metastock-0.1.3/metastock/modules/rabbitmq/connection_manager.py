import logging

from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.environment import env
from metastock.modules.rabbitmq.connection import RabbitMQConnection

logging.getLogger("pika").setLevel(logging.WARNING)


class RabbitMQConnectionManager:
    INSTANCE = None
    _is_inited = False
    _connections = {}

    def initialize(self):
        if self._is_inited:
            return

        # init default connection
        self._init_default_connection()

    def _init_default_connection(self):
        host = env().get("RABBITMQ_DEFAULT_CONNECTION_HOST")
        port = env().get("RABBITMQ_DEFAULT_CONNECTION_PORT")
        username = env().get("RABBITMQ_DEFAULT_CONNECTION_USERNAME")
        password = env().get("RABBITMQ_DEFAULT_CONNECTION_PASSWORD")

        if host and port and username and password:
            Logger().info("Initializing the default RabbitMQ connection...")
            connection = RabbitMQConnection(
                host=host, port=port, username=username, password=password
            )
            connection.connect()

            self._connections["default"] = connection

    def get_connection(self, name="default"):
        connection_instance: RabbitMQConnection = self._connections.get(name)

        return connection_instance


def rabbitmq_manager():
    if RabbitMQConnectionManager.INSTANCE is None:
        RabbitMQConnectionManager.INSTANCE = RabbitMQConnectionManager()

    return RabbitMQConnectionManager.INSTANCE
