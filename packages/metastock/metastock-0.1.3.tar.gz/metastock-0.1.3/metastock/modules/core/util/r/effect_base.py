from abc import ABC, abstractmethod


class EffectBase(ABC):
    @abstractmethod
    def effect(self, r):
        pass
