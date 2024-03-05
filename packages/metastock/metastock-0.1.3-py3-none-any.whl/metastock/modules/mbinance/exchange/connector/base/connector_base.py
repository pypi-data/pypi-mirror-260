from abc import ABC

from metastock.modules.core.logging.logger import AppLogger


class ConnectorBase(ABC):
    def __init__(self, logger: AppLogger = None):
        self._logger = logger
