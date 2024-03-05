from metastock.modules.core.logging.logger import Logger
from metastock.modules.trade.generator.predefined_strategy_generator import PredefinedStrategyGenerator
import sys

try:
    generator = PredefinedStrategyGenerator(
        predefined_input="fixture/trade/predefined_inputs/generator/simple_alert_v1.json"
    )

    generator.generate()
except Exception as e:
    Logger().error("An error occurred: %s", e, exc_info=True)
finally:
    sys.exit(1)
