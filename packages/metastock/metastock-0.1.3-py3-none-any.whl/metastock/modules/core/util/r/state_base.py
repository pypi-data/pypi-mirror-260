from abc import abstractmethod, ABC
from typing import Any

from pyrsistent import PRecord

from metastock.modules.core.util.r.action import Action


class StateBase(PRecord, ABC):
    @abstractmethod
    def reduce(self, action: Action | None = None) -> Any:
        pass
