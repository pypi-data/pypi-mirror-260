from metastock.modules.core.decorator.run_once import run_once
from metastock.modules.rabbitmq.consumer_manager import consumer_manager
from metastock.modules.rabbitmq.job_consumer import JobConsumer
from metastock.modules.test.consumer.test_consumer import TestConsumer
from metastock.modules.test.consumer.test_job_worker1 import TestJobWorker1
from metastock.modules.test.consumer.test_job_worker2 import TestJobWorker2
from metastock.modules.trade.consumer.strategy_consumer import StrategyConsumer
from metastock.modules.trade.consumer.workers.analysis_worker import StockTradingAnalysisWorker


@run_once
def init_queue_config():
    consumer_manager().add_consumer(
            [
                TestConsumer(),
                StrategyConsumer(),
                JobConsumer(
                        name='test_job_consumer',
                        exchange='testbed.exchange',
                        queue='testbed.python.job.consumer.queue',
                        routing_key='testbed.python.job.consumer.key',
                        workers=[
                            TestJobWorker1,
                            TestJobWorker2
                        ]
                ),
                JobConsumer(
                        name='stock_trading_analysis_job_consumer',
                        exchange='stock.trading.analysis.exchange',
                        queue='stock.trading.analysis.job.queue',
                        routing_key='stock.trading.analysis.job.queue.key',
                        workers=[
                            StockTradingAnalysisWorker
                        ]
                )
            ]
    )
