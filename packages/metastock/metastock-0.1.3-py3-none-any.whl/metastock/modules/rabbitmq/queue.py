import pika

from metastock.modules.core.logging.logger import Logger


class RabbitMQQueue:
    def __init__(self, connection: pika.BlockingConnection):
        self.connection = connection
        self.channel = self.connection.channel()

    def _declare_queue(self, queue: str):
        result = self.channel.queue_declare(queue=queue, durable=True, exclusive=False)
        Logger().info(f"Queue '{result.method.queue}' declared.")

        return result.method.queue

    def _declare_exchange(self, exchange: str):
        self.channel.exchange_declare(
            exchange=exchange, exchange_type="topic", durable=True, passive=False
        )

    def delete_queue(self, queue_name):
        self.channel.queue_delete(queue=queue_name)
        Logger().info(f"Queue '{queue_name}' deleted.")

    def bind_queue(self, exchange: str, queue: str, routing_key: str):
        # make sure exchange existed
        self._declare_exchange(exchange)
        self._declare_queue(queue)

        self.channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)
