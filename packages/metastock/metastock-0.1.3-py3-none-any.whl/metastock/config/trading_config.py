from metastock.modules.core.decorator.run_once import run_once
from metastock.modules.core.logging.logger import Logger
from metastock.modules.trade.strategy.actions.action_manager import action_manager
from metastock.modules.trade.strategy.actions.alert_action_v1 import AlertActionV1
from metastock.modules.trade.strategy.actions.fixed_buy_action_v1 import (
    FixedBuyActionV1,
)
from metastock.modules.trade.strategy.actions.simple_action_v1 import SimpleActionV1
from metastock.modules.trade.strategy.assessor.accessor_manager import accessor_manager
from metastock.modules.trade.strategy.assessor.simple_buy_assessor import (
    SimpleBuyAssessor,
)
from metastock.modules.trade.strategy.filters.capitalization_filter import (
    CapitalizationFilter,
)
from metastock.modules.trade.strategy.filters.filter_manager import filter_manager
from metastock.modules.trade.strategy.filters.specific_symbols_filter import (
    SpecificSymbolsFilter,
)
from metastock.modules.trade.strategy.filters.total_trade_value_filter import (
    TotalTradeValueFilter,
)
from metastock.modules.trade.strategy.signals.analysis.tick_signal import TickSignal
from metastock.modules.trade.strategy.signals.signal_manager import signal_manager
from metastock.modules.trade.strategy.signals.technical.hullma_singal import (
    HullmaSignal,
)
from metastock.modules.trade.strategy.signals.technical.simple_sqz_mom_signal import (
    SimpleSqzMomSignal,
)
from metastock.modules.trade.strategy.simple_strategy_v1 import SimpleStrategyV1
from metastock.modules.trade.strategy.strategy_manager import strategy_manager

# ______________ STRATEGY ______________
STRATEGIES = {SimpleStrategyV1.name: {"class": SimpleStrategyV1}}

# ______________ STRATEGY_FILTER ______________
TRADING_STRATEGY_FILTERS = {
    CapitalizationFilter.name: {"class": CapitalizationFilter},
    SpecificSymbolsFilter.name: {"class": SpecificSymbolsFilter},
    TotalTradeValueFilter.name: {"class": TotalTradeValueFilter},
}

# ______________ STRATEGY_SIGNAL ______________

TRADING_STRATEGY_SIGNALS = {
    SimpleSqzMomSignal.name: {"class": SimpleSqzMomSignal},
    HullmaSignal.name: {"class": HullmaSignal},
    TickSignal.name: {"class": TickSignal},
}

# ______________ STRATEGY_ACTION ______________
TRADING_STRATEGY_ACTIONS = {
    SimpleActionV1.name: {"class": SimpleActionV1},
    AlertActionV1.name: {"class": AlertActionV1},
    FixedBuyActionV1.name: {"class": FixedBuyActionV1},
}

# ______________ STRATEGY_ACCESSOR ______________
TRADING_STRATEGY_ACCESSORS = {
    SimpleBuyAssessor.name: {"class": SimpleBuyAssessor},
}


@run_once
def init_trading_strategy_config():
    Logger().info("Initialize trading strategy config")
    for key, value in STRATEGIES.items():
        strategy_manager().define(key, value)

    for key, value in TRADING_STRATEGY_FILTERS.items():
        filter_manager().define(key, value)

    for key, value in TRADING_STRATEGY_ACTIONS.items():
        action_manager().define(key, value)

    for key, value in TRADING_STRATEGY_SIGNALS.items():
        signal_manager().define(key, value)

    for key, value in TRADING_STRATEGY_ACCESSORS.items():
        accessor_manager().define(key, value)
