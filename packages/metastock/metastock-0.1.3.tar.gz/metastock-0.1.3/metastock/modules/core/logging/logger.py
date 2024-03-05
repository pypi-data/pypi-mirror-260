import logging
import os

from dependency_injector.wiring import inject, Provide
from rich.console import Console
from rich.logging import RichHandler
from rich.rule import Rule
from splunk_handler import SplunkHandler

from metastock.modules.core.logging.formatter import CustomJsonFormatter, RichFormatter
from metastock.modules.core.util.environment import is_development

_log_instances = {}


class AppLogger(logging.Logger):
    _console = Console()

    def ok(self, msg, *args, **kwargs):
        self.info(f"[green]OK[/green] {msg}", *args, **kwargs)

    def success(self, msg, *args, **kwargs):
        self.info(f"[green]Success[/green] {msg}", *args, **kwargs)

    def state_update_success(self, msg, *args, **kwargs):
        self.info(f"[green]Success update state[/green] {msg}", *args, **kwargs)

    def will(self, msg, *args, **kwargs):
        self.info(f"[blue]Will[/blue] {msg}", *args, **kwargs)

    def console(self):
        return self._console

    def print_rule(self, text: str = ""):
        self._console.print(Rule(text))

    def set_console_level(self, level):
        for handler in self.handlers:
            if isinstance(handler, RichHandler):
                handler.setLevel(level)


def Logger(name: str = "root") -> AppLogger:
    cached = _log_instances.get(name)
    if cached:
        return cached
    else:
        _logger = AppLogger(name)
        _logger.setLevel(level=logging.DEBUG)

        # Old
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        #
        # ch.setFormatter(CustomFormatter())
        # _logger.addHandler(ch)

        rich_handler = get_rich_logger_handler()
        _logger.addHandler(rich_handler)

        # File logger tạm thời cho error
        if not os.path.exists("logs"):
            os.makedirs("logs")

        # Combine
        # file_handler = logging.FileHandler("logs/combine_logs.log")
        # file_handler.setLevel(logging.DEBUG)
        # formatter = logging.Formatter(
        #     "%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s"
        # )
        # file_handler.setFormatter(formatter)
        # _logger.addHandler(file_handler)
        # Warning/Error
        file_error_handler = logging.FileHandler("logs/error_logs.log")
        file_error_handler.setLevel(logging.WARNING)
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s"
        )
        file_error_handler.setFormatter(formatter)
        _logger.addHandler(file_error_handler)

        # Splunk
        if os.environ.get("SPLUNK_ENABLE") == "true":
            splunk = SplunkHandler(
                host="54.151.152.110",
                protocol="http",
                port=8088,
                token=os.environ.get("SPLUNK_TOKEN"),
                index="metastock",
                # allow_overrides=True # whether to look for _<param in log data (ex: _index)
                debug=False,  # whether to print module activity to stdout, defaults to False
                flush_interval=3.0,
                # send batch of logs every n sec, defaults to 15.0, set '0' to block thread & send immediately
                # force_keep_ahead=True # sleep instead of dropping logs when queue fills
                # hostname='hostname', # manually set a hostname parameter, defaults to socket.gethostname()
                # protocol='http', # set the protocol which will be used to connect to the splunk host
                # proxies={
                #           'http': 'http://10.10.1.10:3128',
                #           'https': 'http://10.10.1.10:1080',
                #         }, set the proxies for the session request to splunk host
                #
                queue_size=0,
                # a throttle to prevent resource overconsumption, defaults to 5000, set to 0 for no max
                # record_format=True, whether the log format will be json
                # retry_backoff=1, the requests lib backoff factor, default options will retry for 1 min, defaults to 2.0
                # retry_count=2, number of retry attempts on a failed/erroring connection, defaults to 5
                source="metastock_" + os.environ.get("ENVIRONMENT"),
                # manually set a source, defaults to the log record.pathname
                sourcetype="_json",  # manually set a sourcetype, defaults to 'text'
                verify=False,  # turn SSL verification on or off, defaults to True
                timeout=5,  # timeout for waiting on a 200 OK from Splunk server, defaults to 60s
            )

            splunk.setFormatter(CustomJsonFormatter("%(level)s %(file)s %(message)s"))
            _logger.addHandler(splunk)

        _log_instances[name] = _logger
        return _log_instances[name]


def get_rich_logger_handler():
    # Tạo một RichHandler để định dạng thông báo log
    handler = RichHandler(
        rich_tracebacks=True if is_development() else False,
        markup=True,
        # console = console.Console(highlight = True)
    )

    handler.setFormatter(RichFormatter())

    return handler


@inject
def get_logger(instance=Provide["logger"]) -> AppLogger:
    return instance
