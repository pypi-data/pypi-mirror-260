import typer

from metastock.cli.pystock import queue_consumer_start

typer.run(queue_consumer_start)
