import os

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table


class Environment:
    instance = None

    def __init__(self, prefix: str):
        self.prefix = prefix

    def get(self, key: str):
        return os.environ.get(f"{self.prefix}_{key}")


def env() -> Environment:
    return Environment.instance


def config_env(prefix: str, dump: bool = True) -> None:
    if Environment.instance is not None:
        return

    Environment.instance = Environment(prefix=prefix)
    if os.environ.get("ENVIRONMENT") is None:
        os.environ.setdefault("ENVIRONMENT", "development")

    if dump:
        dump_env()


def is_development() -> bool:
    return os.environ.get("ENVIRONMENT") in ["development", "local"]


"""
- File nào load trước thì sẽ ưu tiên
"""
current_env = os.environ.get("ENVIRONMENT")

if current_env == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.local")
    load_dotenv(f".env.{current_env}")


def dump_env():
    table = Table(title="Environment")

    table.add_column("Key", justify="left", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("ENVIRONMENT", os.environ.get("ENVIRONMENT"))

    for key, value in os.environ.items():
        # Kiểm tra nếu tên biến môi trường bắt đầu bằng PS_
        if key.startswith(env().prefix):
            table.add_row(key, value)

    console = Console()
    console.print(table, justify="center")
