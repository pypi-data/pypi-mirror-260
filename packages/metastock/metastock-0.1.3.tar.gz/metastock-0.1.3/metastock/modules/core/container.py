from dependency_injector import containers, providers

from metastock.modules.core.db.postgres_manager import PostgresManager
from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.registry import Registry


class CoreContainer(containers.DeclarativeContainer):
    logger = providers.Dependency(instance_of=AppLogger)

    postgres_manager = providers.ThreadSafeSingleton(PostgresManager)
