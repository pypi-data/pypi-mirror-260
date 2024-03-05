import typer

from metastock.cli.mbinance.main import queue_consumer_start

typer.run(queue_consumer_start)
