import pika

from metastock.modules.core.logging.logger import Logger


class RabbitMQConnection:
    def __init__(self, host="localhost", port=5672, username="guest", password="guest"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials,
            # retry_delay=5,
        )
        self.connection = pika.BlockingConnection(parameters)

        # Log connection successful
        Logger().ok("Connected to RabbitMQ!")

        # Register a callback to handle disconnection events
        self.connection.add_on_connection_blocked_callback(self._on_connection_blocked)
        self.connection.add_on_connection_unblocked_callback(
            self._on_connection_unblocked
        )

    def _on_connection_blocked(self, _unused_frame):
        Logger().info("Connection blocked!")

    def _on_connection_unblocked(self, _unused_frame):
        Logger().info("Connection unblocked!")

    def _on_connection_closed(self, _unused_connection, reason):
        Logger().info(f"Connection closed: {reason}")
        # Try reconnecting
        self.connect()

    def get_rabbit_connection(self):
        if not self.connection or self.connection.is_closed:
            self.connect()
        return self.connection
