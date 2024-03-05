import arrow
from marshmallow import fields, Schema, validate
from rich.table import Table

from metastock.modules.core.logging.logger import Logger
from metastock.modules.trade.strategy.assessor.abstract_accessor import AbstractAccessor


class TSchema(Schema):
    min = fields.Integer()
    max = fields.Integer()


class InputSchema(Schema):
    t = fields.Nested(TSchema)
    roi = fields.Float(validate=validate.Range(min=0))


class SimpleBuyAccessorDefaultSchema(Schema):
    api = fields.String()
    input = fields.Nested(InputSchema)


class SimpleBuyAccessorDefaultConfig:
    def __init__(self):
        self.min_t = 2
        self.max_t = 4
        self.roi = 1.01


class SimpleBuyAssessor(AbstractAccessor):
    name = "simple_buy_accessor_v1"

    def __init__(self):
        super().__init__()
        self.config = None
        self.result = {}

    def before_run(self):
        input_config = self.get_input_config()["input"]
        SimpleBuyAccessorDefaultSchema().validate(self.get_input_config())
        self.config = SimpleBuyAccessorDefaultConfig()

        if "t" in input_config:
            min_t = input_config["t"].get("min")
            max_t = input_config["t"].get("max")

            if isinstance(max_t, int) and max_t > 3:
                self.config.max_t = max_t

            if isinstance(min_t, int) and 2 < min_t < max_t:
                self.config.min_t = min_t

        if input_config["roi"] > 1:
            self.config.roi = input_config["roi"]

        Logger().info(f"Use config {self.config} for access")

    def access(self, strategy_process, process_actions, history_price):
        symbol = strategy_process["symbol"]
        Logger().will(f"access for symbol {symbol} by SimpleBuyAssessor")

        if symbol in self.result:
            Logger().warning(f"Duplicate access for symbol {symbol}")
        else:
            self.result[symbol] = {"pass": [], "fail": [], "percent": 0}

        for action in process_actions:
            date = action["date"]
            a_date = arrow.get(date)
            # min_date = a_date.shift(days=self.config.min_t)
            # do co t7,cn hoac ngay le
            max_date = a_date.shift(days=self.config.max_t + 10)

            def is_valid_min_max_day(price_day):
                a_price_day = arrow.get(price_day["date"])

                return a_date <= a_price_day <= max_date

            look_up_days = [
                price_day
                for price_day in history_price
                if is_valid_min_max_day(price_day)
            ]
            look_up_days = sorted(look_up_days, key=lambda x: x["date"], reverse=False)
            look_up_days = look_up_days[self.config.min_t : self.config.max_t + 1]

            result = next(
                (
                    obj
                    for obj in look_up_days
                    if max(obj["rHigh"], obj["rClose"]) / action["meta"]["price"]
                    >= self.config.roi
                ),
                None,
            )

            if result is not None:
                self.result[symbol]["pass"].append(action)
            else:
                self.result[symbol]["fail"].append(action)

        self.result[symbol]["percent"] = round(
            len(self.result[symbol]["pass"])
            / (len(self.result[symbol]["pass"]) + len(self.result[symbol]["fail"])),
            2,
        )
        Logger().info(f"{symbol} has percent '{self.result[symbol]['percent']}'")

    def run(self):
        super().run()
        self._summary()

    def _summary(self):
        table = Table(title="Summary")
        table.add_column("Cổ Phiếu", justify="left", style="cyan", no_wrap=True)
        table.add_column("Phần trăm", style="magenta")
        table.add_column("Pass", style="magenta")
        table.add_column("Fail", style="magenta")

        # Sắp xếp lại dictionary theo giá trị percent
        sorted_result = dict(
            sorted(self.result.items(), key=lambda x: x[1]["percent"], reverse=True)
        )

        # Duyệt qua từng phần tử trong dictionary đã sắp xếp
        for symbol, data in sorted_result.items():
            table.add_row(
                f"{symbol}",
                f'{data["percent"]}',
                f"{len(data['pass'])}",
                f"{len(data['fail'])}",
            )

        total_percent = 0
        num_symbols = len(self.result)

        for symbol_data in self.result.values():
            total_percent += symbol_data["percent"]

        # Tính trung bình
        average_percent = round(total_percent / num_symbols, 2)
        table.add_row("AVG percent", f"{average_percent}", "", "")
        Logger().console().print(table, justify="center")
