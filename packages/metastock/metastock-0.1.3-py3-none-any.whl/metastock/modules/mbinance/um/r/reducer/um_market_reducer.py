from pandas import DataFrame
from pyrsistent import field, PRecord

from metastock.modules.core.util.r.action import Action


class UmMarketState(PRecord):
    klines = field(type=(DataFrame, type(None)))


def um_market_reducer(state: UmMarketState, action: Action) -> UmMarketState:
    if state is None:
        state = UmMarketState(klines=None)

    return state
