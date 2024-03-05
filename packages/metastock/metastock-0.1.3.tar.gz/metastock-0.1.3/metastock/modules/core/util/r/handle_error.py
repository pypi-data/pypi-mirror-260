from metastock.modules.core.logging.logger import Logger
from metastock.modules.mbinance.error.fatal_error import FatalError


def handle_error(error):
    if isinstance(error, FatalError):
        Logger().error("Fatal error in subscribe, will close application")

    Logger().exception(error)
