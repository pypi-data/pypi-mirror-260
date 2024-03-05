from dependency_injector.wiring import inject, Provide

from metastock.cli.mbinance.config.queue_config import mbinance_queue_config
from metastock.modules.core.db.postgres_manager import postgres_manager
from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.rabbitmq.connection_manager import rabbitmq_manager
from metastock.modules.rabbitmq.consumer_manager import consumer_manager


@inject
def queue_consumer_start_cmd(name: str, logger: AppLogger = Provide["core.logger"]):
    postgres_manager.initialize()
    rabbitmq_manager().initialize()
    mbinance_queue_config(logger=logger)
    consumer = consumer_manager().get_consumer(name)

    if consumer is not None:
        consumer.run()
