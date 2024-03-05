from abc import ABC
from typing import Type

from marshmallow import ValidationError

from metastock.modules.core.logging.logger import Logger
from metastock.modules.rabbitmq.consumer import RabbitMQConsumer
from metastock.modules.rabbitmq.job_worker import JobWorker
from metastock.modules.rabbitmq.schema import job_consumer_body_schema


class JobConsumer(RabbitMQConsumer, ABC):
    def __init__(
            self,
            name: str,
            exchange: str,
            queue: str,
            routing_key: str,
            workers: list[Type[JobWorker]],
            connection='default'
    ):
        self.workers = workers
        self.name = name
        super().__init__(exchange=exchange, queue=queue, routing_key=routing_key, connection=connection)

    def get_name(self):
        return self.name

    def handle_message(self, ch, method, properties, body):
        Logger().info(f"Received message: {body.decode()}")
        try:
            data = job_consumer_body_schema.loads(body.decode("utf-8"))
            job_id = data.get('job_id')
            worker_class: Type[JobWorker] = next(filter(lambda w: w.job_id == job_id, self.workers), None)

            if worker_class:
                # Make sure new instance of worker is created when receiving new message
                worker = worker_class()
                worker.handle(ch, method, properties, body)
            else:
                Logger().warning(f"Not found any worker can consume job {job_id}")

            ch.basic_ack(delivery_tag=method.delivery_tag)
            Logger().info("Message acknowledged.")

        except ValidationError as e:
            Logger().error("Error validate request body: %s", e, exc_info=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            Logger().error("Error: %s", e, exc_info=True)

            # Negative Acknowledge the message
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            Logger().warning("Message NOT acknowledged")
