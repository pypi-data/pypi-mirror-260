from pyrsistent import field, PRecord

from metastock.modules.core.util.r.action import Action, match_action
from metastock.modules.mbinance.um.r.actions.save_time_diff import (
    save_time_diff_action,
)


class UmCommonState(PRecord):
    time_diff = field(type=(float, type(None)))


def um_common_reducer(state: UmCommonState, action: Action) -> UmCommonState:
    if state is None:
        state = UmCommonState(time_diff=None)

    if action is None:
        return state

    if match_action(action, save_time_diff_action):
        state = state.set("time_diff", action.payload)

    return state
