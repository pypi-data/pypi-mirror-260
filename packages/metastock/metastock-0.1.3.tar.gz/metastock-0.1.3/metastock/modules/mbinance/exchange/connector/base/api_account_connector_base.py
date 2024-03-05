from abc import abstractmethod

from reactivex.subject import BehaviorSubject

from metastock.modules.mbinance.exchange.connector.base.connector_base import (
    ConnectorBase,
)


class ApiAccountConnectorBase(ConnectorBase):

    """
    - SIMULATE
    - Publish những thông tin liên quan đến user (order/balance)
    """

    _api_user_data_ob: BehaviorSubject[any] = BehaviorSubject(value=None)

    def get_api_user_data_ob(self) -> BehaviorSubject:
        return self._api_user_data_ob

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def get_account_balance(self):
        pass

    @abstractmethod
    def get_positions(self):
        pass

    @abstractmethod
    def stop(self):
        pass
