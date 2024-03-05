import arrow

from metastock.modules.core.logging.logger import Logger
from metastock.modules.stockinfo.ulti.get_tick_history import get_tick_history
from metastock.modules.trade.analysis.tick import (
    AnalysisTickConfig,
    StockTradingAnalysisTick,
)
from metastock.modules.trade.strategy.signals.output_schema import (
    SIGNAL_OUTPUT_SCHEMA_V1_NAME,
)
from metastock.modules.trade.strategy.signals.signal_abstract import SignalAbstract


class TickSignal(SignalAbstract):
    name = "tick_shark_signal"

    def get_output(self, version="v1"):
        Logger().info("Will generate TickSignal output v1 ")
        ticks = get_tick_history(
            symbol=self.strategy.get_symbol(),
            from_date=self.strategy.get_from_date(),
            to_date=self.strategy.get_to_date(),
        )
        input_data = self.get_input()

        tick_config = AnalysisTickConfig()
        if "tick_shark_signal" in input_data:
            Logger().info(
                f"Has config for tick_shark_signal in strategy input: {input_data['tick_shark_signal']}"
            )
            tick_config.trade_value = input_data["tick_shark_signal"]["trade_value"]
            tick_config.shark_collect_percent = input_data["tick_shark_signal"][
                "shark_collect_percent"
            ]

        collected_days = []
        Logger().will(f"process analyzing tick data for {len(ticks)} days...")
        for tick in ticks:
            tick_analysis = StockTradingAnalysisTick(tick_data=tick, config=tick_config)
            data = tick_analysis.get_data()

            if data["is_shark_collect"]:
                collected_days.append(
                    {
                        "date": arrow.get(tick["date"]).format("YYYY-MM-DD"),
                        "p": data["shark_collect_from_price"],
                    }
                )

        return {"buy": collected_days}

    def support_output_versions(self) -> list[str]:
        return [SIGNAL_OUTPUT_SCHEMA_V1_NAME]
