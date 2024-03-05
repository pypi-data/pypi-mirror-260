from metastock.modules.rabbitmq.consumer import RabbitMQConsumer


class TestConsumer(RabbitMQConsumer):
    name = "test_consumer"

    def __init__(self):
        super().__init__(
            exchange="testbed.exchange",
            queue="testbed.python.queue",
            routing_key="testbed.routing.key",
        )

    def get_name(self):
        return "test_consumer"
