from pyrsistent import PRecord, pvector, pvector_field

from metastock.modules.core.logging.logger import get_logger
from metastock.modules.core.util.r.action import Action
from metastock.modules.mbinance.um.api_schema.response.account_balance_v2 import (
    AccountBalanceResponse,
    AccountBalanceResponseItem,
)
from metastock.modules.mbinance.um.r.actions.ac_005_get_account_balance_success import (
    AC_005_GET_ACCOUNT_BALANCE_SUCCESS,
)
from metastock.modules.mbinance.um.util.fmt_state_update_action import (
    fmt_state_update_action,
)


class UmAccountState(PRecord):
    balances = pvector_field(AccountBalanceResponseItem)


def um_account_reducer(state: UmAccountState, action: Action) -> UmAccountState:
    if state is None:
        state = UmAccountState(balances=pvector())

    if action is None:
        return state

    match action.name:
        case AC_005_GET_ACCOUNT_BALANCE_SUCCESS.name:
            account_balance_res: AccountBalanceResponse = action.payload
            state = state.set("balances", pvector(account_balance_res.data))
            get_logger().info(
                f"{fmt_state_update_action(AC_005_GET_ACCOUNT_BALANCE_SUCCESS.name)} -> Updated account balances"
            )

    return state
