import json
from time import sleep

from metastock.modules.core.logging.logger import Logger
from metastock.modules.rabbitmq.consumer import RabbitMQConsumer
from metastock.modules.trade.error import StrategyNotFound, UnknownMessageFromQueue
from metastock.modules.trade.request.get_strategy_process import get_strategy_process
from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract
from metastock.modules.trade.strategy.strategy_manager import strategy_manager


class StrategyConsumer(RabbitMQConsumer):
    name = "strategy_process"

    def __init__(self):
        super().__init__(
            exchange="stock.trading.exchange",
            queue="stock.trading.strategy.queue",
            routing_key="stock.trading.strategy",
        )
        self.logger = Logger()

    def get_name(self):
        return StrategyConsumer.name

    def handle_message(self, ch, method, properties, body):
        self.logger.print_rule("START: StrategyConsumer")
        try:
            self.logger.info(f"Received message: {body.decode()}")
            data: dict = json.loads(body.decode("utf-8"))
            if not isinstance(data, dict):
                raise UnknownMessageFromQueue()

            hash_key = data.get("hash")
            symbol = data.get("symbol")

            if hash_key is None or symbol is None:
                raise UnknownMessageFromQueue()

            self.logger.info(
                "Will send request to API downstream to get strategy process"
            )
            strategy_data: dict = get_strategy_process(hash_key=hash_key, symbol=symbol)
            self.logger.info(f"Strategy process data from downstream {strategy_data}")

            if strategy_data.get("state") != 0:
                self.logger.info("skip because state is not pending")
            else:
                strategy_class = strategy_manager().get_class(strategy_data.get("name"))
                self.logger.info(f"use strategy class {strategy_class}")
                if strategy_class is None:
                    raise StrategyNotFound()

                strategy: StrategyAbstract = strategy_class()
                self.logger.info(
                    f"Will process strategy [blue]{strategy.get_name()}[/blue]"
                )

                strategy.load_input(
                    input_config=strategy_data.get("input"),
                    from_date=strategy_data.get("from"),
                    to_date=strategy_data.get("to"),
                )
                strategy.set_symbol(symbol).set_hash(hash_key)
                strategy.execute()

            ch.basic_ack(delivery_tag=method.delivery_tag)
            Logger().info("Message acknowledged.")
            # sleep(500)
        except Exception as e:
            Logger().error("An error occurred: %s", e, exc_info=True)
            # Negative Acknowledge the message
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            Logger().warning("Message not acknowledged, re-queued.")
            sleep(5)

        self.logger.print_rule("END: StrategyConsumer")
