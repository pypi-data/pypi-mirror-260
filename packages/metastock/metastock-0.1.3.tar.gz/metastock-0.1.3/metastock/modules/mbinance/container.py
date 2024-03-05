from dependency_injector import containers, providers

from metastock.modules.core.container import CoreContainer
from metastock.modules.mbinance.um.container import UmContainer


class MBinanceContainer(containers.DeclarativeContainer):
    core: CoreContainer = providers.DependenciesContainer()
    logger = core.logger
    um: UmContainer = providers.Container(UmContainer, core=core)
