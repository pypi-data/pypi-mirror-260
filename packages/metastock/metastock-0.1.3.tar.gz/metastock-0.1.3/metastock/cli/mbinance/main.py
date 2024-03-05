import logging
from typing import Annotated

import typer

from metastock.cli.app import get_typer_cli_app
from metastock.cli.mbinance.application import Application
from metastock.cli.mbinance.cmd.exchange_info_search_symbol_cmd import (
    exchange_info_search_symbol_cmd,
)
from metastock.cli.mbinance.cmd.history_init_candlestick_cmd_v2 import (
    history_init_candlestick_cmd_v2,
)
from metastock.cli.mbinance.cmd.queue_consumer_start_cmd import queue_consumer_start_cmd
from metastock.cli.mbinance.cmd.trade import trade_cmd
from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.environment import config_env
from metastock.modules.mbinance.um.exchange.general.time.get_last_minutes import (
    get_last_minutes,
)
from metastock.modules.mbinance.um.exchange.general.time.get_server_time import (
    get_server_time_ms,
)
from metastock.modules.mbinance.um.util.is_value_in_time_interval import (
    is_value_in_time_interval,
)
from metastock.modules.mbinance.um.value.um_value import UMValue

app = get_typer_cli_app()
logger = Logger()
logger.set_console_level(logging.INFO)
config_env("BN")
container = Application(logger=logger)
container.wire(
    packages=[
        "metastock.cli.mbinance.cmd",
        "metastock.cli.mbinance.config",
        "metastock.modules.core.logging",
    ]
)


@app.command(name="trade")
def trade(pair: Annotated[str, typer.Argument()] = "BTCUSDT"):
    UMValue.set_PAIR(pair=pair)
    trade_cmd(pair=pair)


@app.command(name="g:server-time")
def get_server_time_cmd():
    logger.info(f"Server time: {get_server_time_ms()}")


@app.command(name="g:last-minute")
def get_last_minutes_cmd(minutes: Annotated[int, typer.Argument()] = 1):
    logger.info(f"Last {minutes} minutes time: {get_last_minutes(minutes)}")


@app.command(name="history:init:candlestick:v2")
def history_init_candlestick_v2(
    pair: Annotated[str, typer.Argument()] = "BTCUSDT",
    interval: Annotated[str, typer.Argument()] = "1m",
):
    if not is_value_in_time_interval(interval):
        logger.error(f"Invalid interval: {interval}")
    history_init_candlestick_cmd_v2(pair=pair, interval=interval)


@app.command(name="exchange:info:search:symbol")
def exchange_info_search_symbol(symbol: Annotated[str, typer]):
    exchange_info_search_symbol_cmd(symbol=symbol)


# @app.command(name="history:init:trade_list")
# def history_init_trade_list():
#     try:
#         postgres_manager.initialize()
#
#         end_time = get_server_time_ms()
#         start_time = int(
#             arrow.get(end_time / 1000).shift(minutes=-240).timestamp() * 1000
#         )
#         aggregate_trade_fetcher = AggregateTradeFetcher(
#             start_time=start_time, end_time=end_time
#         )
#         aggregate_trade_fetcher.fetch()
#
#     except Exception as e:
#         logger.exception(e)


@app.command(name="queue:consumer:start")
def queue_consumer_start(
    name: Annotated[str, typer.Argument(help="Name of consumer.")]
):
    queue_consumer_start_cmd(name=name)


@app.command()
def main():
    print(f"Hello")
