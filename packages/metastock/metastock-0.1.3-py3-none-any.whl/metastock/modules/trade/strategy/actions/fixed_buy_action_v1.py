from marshmallow import ValidationError

from metastock.modules.core.logging.logger import Logger
from metastock.modules.trade.strategy.actions.action_abstract import ActionAbstract
from metastock.modules.trade.strategy.signals.output_schema import (
    FixedBuySchema,
    SIGNAL_OUTPUT_SCHEMA_V1_NAME,
)
from metastock.modules.trade.strategy.signals.signal_abstract import SignalAbstract
from metastock.modules.trade.strategy.strategy_abstract import StrategyAbstract


class FixedBuyActionV1(ActionAbstract):
    name = "fixed_buy_action_v1"

    def support_signal_output_versions(self) -> list[str]:
        return [SIGNAL_OUTPUT_SCHEMA_V1_NAME]

    def run(self, strategy: StrategyAbstract, signals: list[SignalAbstract]):
        buy_actions = []

        for signal in signals:
            version_compatible = self._get_compatible_versions(signal).pop(0)

            signal_output = signal.get_output(version_compatible)

            try:
                FixedBuySchema().load(signal_output)

                Logger().info(
                    f"Detected {len(signal_output['buy'])} days has buy signal"
                )

                for buy_data in signal_output["buy"]:
                    buy_actions.append(
                        {"date": buy_data["date"], "price": buy_data["p"]}
                    )
            except ValidationError:
                Logger().warning(
                    f"fixed_buy_action_v1 can not process output of signal: {signal.name}"
                )
            except Exception as e:
                Logger().warning(
                    f"fixed_buy_action_v1 could not process output of signal: {signal.name}"
                )

        # TODO: need to handle when have multiple signal

        # Assume we already processed and had data for buy actions
        # TODO: first we have to retrieve bulk_action_data and update for previous actions

        # then we re-save bulk_action_data
        strategy.set_bulk_action(bulk_action_data={"buy": buy_actions})
