from metastock.modules.core.logging.logger import Logger
from metastock.modules.trade.strategy.strategy_abstract import (
    StrategyAbstract,
    TradingStrategyState,
)


class SimpleStrategyV1(StrategyAbstract):
    name = "simple_strategy_v1"

    def load_input(
        self, input_config: dict, from_date: str = None, to_date: str = None
    ):
        super().load_input(input_config, from_date, to_date)

    def get_input_description(self):
        return {}

    def execute(self):
        super().execute()
        self.mark_process_state(state=TradingStrategyState.Processing)

        try:
            # TODO: Process filter in runtime, global filter already run in generator

            # Process action
            for action in self.actions:
                action.run(self, self.signals)

            self.bulk_submit_action()
            self.mark_process_state(state=TradingStrategyState.Complete)
        except Exception as e:
            Logger().error(
                f"Could not execute strategy '{self.name}' {e}", exc_info=True
            )
            self.mark_process_state(state=TradingStrategyState.Error)
