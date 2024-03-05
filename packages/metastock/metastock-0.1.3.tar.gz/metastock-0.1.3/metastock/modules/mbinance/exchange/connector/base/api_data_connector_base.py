import abc

from reactivex.subject import BehaviorSubject

from metastock.modules.mbinance.exchange.connector.base.connector_base import (
    ConnectorBase,
)


class ApiDataConnectorBase(ConnectorBase):

    """
    - SIMULATE
    - Publish data để context có thể subscribe lấy dữ liệu,
    - Sau này nếu giả lập thì mình chỉ cần bắn data vào observable này
    """

    _api_market_data_ob: BehaviorSubject[any] = BehaviorSubject(value=None)

    def get_api_market_data_ob(self) -> BehaviorSubject:
        """
        - Lấy dữ liệu market chỉ quan tâm duy nhất đến observer này.

        :return:
        """
        return self._api_market_data_ob

    @abc.abstractmethod
    def initialize(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass
