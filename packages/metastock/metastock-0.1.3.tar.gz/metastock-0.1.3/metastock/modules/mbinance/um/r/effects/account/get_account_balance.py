from reactivex import compose, operators as ops

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.r.effect_base import EffectBase
from metastock.modules.core.util.r.rx_common import of_type
from metastock.modules.mbinance.exchange.connector.base.api_account_connector_base import (
    ApiAccountConnectorBase,
)
from metastock.modules.mbinance.um.r.actions.ac_003_account_balance_update import (
    AC_003_ACCOUNT_UPDATE,
)
from metastock.modules.mbinance.um.r.actions.ac_004_get_account_balance import (
    AC_004_GET_ACCOUNT_BALANCE,
)
from metastock.modules.mbinance.um.r.actions.ac_005_get_account_balance_success import (
    AC_005_GET_ACCOUNT_BALANCE_SUCCESS,
)
from metastock.modules.mbinance.um.r.actions.ac_006_get_account_balance_error import (
    AC_006_GET_ACCOUNT_BALANCE_ERROR,
)


class GetAccountBalanceEffect(EffectBase):
    def __init__(
        self, api_account_connector: ApiAccountConnectorBase, logger: AppLogger
    ):
        super().__init__()
        self._logger = logger
        self._api_account_connector = api_account_connector

    def effect(self, _):
        def __get_account_balance(_):
            self._logger.debug("Getting account balance")
            try:
                balance = self._api_account_connector.get_account_balance()
                self._logger.debug("OK get account balance: {}".format(balance))
                return AC_005_GET_ACCOUNT_BALANCE_SUCCESS(balance)
            except Exception as e:
                return AC_006_GET_ACCOUNT_BALANCE_ERROR(e)

        return compose(
            of_type(AC_003_ACCOUNT_UPDATE, AC_004_GET_ACCOUNT_BALANCE),
            ops.map(__get_account_balance),
        )
