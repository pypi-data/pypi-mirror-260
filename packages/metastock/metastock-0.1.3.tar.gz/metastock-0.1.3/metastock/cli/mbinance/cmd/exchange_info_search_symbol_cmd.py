from dependency_injector.wiring import inject, Provide
from rich.table import Table

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.mbinance.um.exchange.general.exchange_info import (
    get_exchange_info,
)
from metastock.modules.mbinance.um.value.um_value import UMValue


@inject
def exchange_info_search_symbol_cmd(
    symbol: str, logger: AppLogger = Provide["core.logger"]
):
    exchange_info = get_exchange_info()
    symbols = exchange_info.get("symbols")
    data = []
    if isinstance(symbols, list):
        for s in symbols:
            if (
                symbol in s.get("baseAsset")
                and s.get("contractType") == UMValue.CONTRACT_TYPE
            ):
                data.append(s.get("pair"))

    table = Table(title="List of Pair")
    table.add_column("Index")
    table.add_column("String")

    for index, string in enumerate(data):
        table.add_row(str(index), string)

    logger.console().print(table, justify="center")
