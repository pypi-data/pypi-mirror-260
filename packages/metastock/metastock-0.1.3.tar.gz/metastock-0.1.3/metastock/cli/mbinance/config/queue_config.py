from dependency_injector.wiring import inject

from metastock.modules.core.decorator.run_once import run_once
from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.mbinance.um.trade.strategy.history_test.queue.consumer.msell_v1_consumer import (
    MSellV1Consumer,
)
from metastock.modules.rabbitmq.consumer_manager import consumer_manager
from metastock.modules.test.consumer.test_consumer import TestConsumer


@run_once
@inject
def mbinance_queue_config(logger: AppLogger):
    logger.info("Configure mbinance queue")
    consumer_manager().add_consumer([TestConsumer(), MSellV1Consumer()])
