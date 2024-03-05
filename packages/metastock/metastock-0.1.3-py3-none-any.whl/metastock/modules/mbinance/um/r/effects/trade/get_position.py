from reactivex import compose, operators as ops

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.r.action import Action
from metastock.modules.core.util.r.effect_base import EffectBase
from metastock.modules.core.util.r.rx_common import of_type
from metastock.modules.mbinance.error.fatal_error import FatalError
from metastock.modules.mbinance.exchange.connector.base.api_account_connector_base import (
    ApiAccountConnectorBase,
)
from metastock.modules.mbinance.um.api_schema.response.position_info import (
    PositionInfoResponse,
)
from metastock.modules.mbinance.um.r.actions.order.position.ac_t01_get_position import (
    AC_T01_GET_POSITION,
)
from metastock.modules.mbinance.um.r.actions.order.position.ac_t02_get_position_success import (
    AC_T02_GET_POSITION_SUCCESS,
)
from metastock.modules.mbinance.um.r.actions.order.position.ac_t03_get_position_error import (
    AC_T03_GET_POSITION_ERROR,
)
from metastock.modules.mbinance.um.value.um_value import UMValue


class GetPositionEffect(EffectBase):
    def __init__(
        self, logger: AppLogger, api_account_connector: ApiAccountConnectorBase
    ):
        super().__init__()
        self._logger = logger
        self._api_account_connector = api_account_connector

    def effect(self, r):
        def __get_position(_: Action):
            try:
                res: PositionInfoResponse = self._api_account_connector.get_positions()
                data = list(
                    filter(
                        lambda x: x.symbol == UMValue.SYMBOL(),
                        res.data,
                    )
                )

                if len(data) > 1:
                    raise FatalError("Not support more than one position")

                if len(data) == 0:
                    raise FatalError("No position found. Please check your environment")

                if len(data) == 1:
                    self._logger.info(f"OK get current position info {data}")
                    return AC_T02_GET_POSITION_SUCCESS(data[0])
            except Exception as e:
                self._logger.error("Error getting position info", exc_info=e)
                return AC_T03_GET_POSITION_ERROR({"error": e})

        return compose(of_type(AC_T01_GET_POSITION), ops.map(__get_position))
