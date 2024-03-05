from abc import ABC, abstractmethod

from metastock.modules.core.logging.logger import Logger
from metastock.modules.rabbitmq.connection_manager import rabbitmq_manager
from metastock.modules.rabbitmq.queue import RabbitMQQueue


class RabbitMQConsumer(ABC):
    def __init__(
        self, exchange: str, queue: str, routing_key: str, connection="default"
    ):
        self.connection = connection
        self.routing_key = routing_key
        self.queue = queue
        self.exchange = exchange

    @abstractmethod
    def get_name(self):
        pass

    def handle_message(self, ch, method, properties, body):
        Logger().info(f"Received message: {body.decode()}")
        try:
            # Process the message here
            # ...

            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            Logger().info("Message acknowledged.")
        except Exception as e:
            Logger().error("An error occurred: %s", e, exc_info=True)

            # Negative Acknowledge the message
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            Logger().warning("Message not acknowledged, re-queued.")

    def run(self) -> None:
        exchange = self.exchange
        queue = self.queue
        routing_key = self.routing_key

        rabbit_connection = (
            rabbitmq_manager()
            .get_connection(name=self.connection)
            .get_rabbit_connection()
        )
        rabbit_queue = RabbitMQQueue(rabbit_connection)

        #  bind queue to exchange
        rabbit_queue.bind_queue(exchange=exchange, queue=queue, routing_key=routing_key)

        channel = rabbit_connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=queue,
            on_message_callback=self.handle_message,
            auto_ack=False,
            exclusive=False,
        )

        Logger().info(
            f" [*] Waiting for queue [bold blue]{queue}[/bold blue] routing key [bold blue]{routing_key}[/bold blue]. To exit press CTRL+C"
        )
        channel.start_consuming()
