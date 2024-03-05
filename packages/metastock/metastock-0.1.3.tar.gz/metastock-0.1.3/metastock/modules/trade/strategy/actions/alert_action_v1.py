from metastock.modules.core.logging.logger import Logger
from metastock.modules.core.util.datetime.check_recent_date import check_recent_date
from metastock.modules.core.util.write_to_file import write_to_file
from metastock.modules.trade.strategy.actions.action_abstract import ActionAbstract
from metastock.modules.trade.strategy.signals.output_schema import SIGNAL_OUTPUT_SCHEMA_V1_NAME
from metastock.modules.trade.strategy.signals.signal_abstract import SignalAbstract
from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract


class AlertActionV1(ActionAbstract):
    name = 'alert_action_v1'

    def support_signal_output_versions(self) -> list[str]:
        return [SIGNAL_OUTPUT_SCHEMA_V1_NAME]

    def run(self, strategy: StrategyAbstract, signals: list[SignalAbstract]):
        for signal in signals:
            version_compatible = self._get_compatible_versions(signal).pop(0)

            signal_output = signal.get_output(version_compatible)

            price_history = self.get_strategy().get_price_history()

            for price in price_history:
                date: str = price['date']
                if check_recent_date(date, 4):
                    Logger().info(f"Symbol '{self.strategy.get_symbol()}' checking alerting for date '{date}'")
                    # work for alert
                    current_date_signal = next((item for item in signal_output if item['date'] == date), None)
                    alert = current_date_signal.get('alert')
                    is_noty = alert.get('notify')

                    if is_noty:
                        Logger().info(f"{alert.get('message')}")
                        write_to_file(f"{alert.get('message')}", "check_symbol.log")
