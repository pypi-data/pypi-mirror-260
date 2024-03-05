from abc import ABC, abstractmethod, abstractproperty


class JobWorker(ABC):

    job_id = ''

    @abstractmethod
    def handle(self, ch, method, properties, body):
        pass
