from metastock.modules.core.logging.logger import Logger
from metastock.modules.rabbitmq.job_worker import JobWorker


class TestJobWorker2(JobWorker):
    job_id = 'test_job_worker_2'

    def handle(self, ch, method, properties, body):
        Logger().info('Process TestJobWorker2')
