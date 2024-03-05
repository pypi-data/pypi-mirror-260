from dependency_injector import containers, providers

from metastock.modules.core.container import CoreContainer
from metastock.modules.mbinance.container import MBinanceContainer


class Application(containers.DeclarativeContainer):
    # config = providers.Configuration(yaml_files=["config.yml"])
    logger = providers.Dependency()
    core = providers.Container(CoreContainer, logger=logger)

    mbinance: MBinanceContainer = providers.Container(
        MBinanceContainer,
        core=core,
    )
