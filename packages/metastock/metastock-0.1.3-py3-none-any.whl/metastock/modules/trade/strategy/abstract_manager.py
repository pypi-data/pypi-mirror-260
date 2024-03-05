from abc import ABC
from typing import Any


class AbstractManager(ABC):
    INSTANCE = None

    def __init__(self):
        self.class_map = {}

    def define(self, key: str, spec: Any):
        self.class_map[key] = spec

    def get_class_map(self) -> dict:
        return self.class_map

    def get_class(self, name: str):
        if name is None:
            return None

        _map = self.class_map.get(name)

        if isinstance(_map, dict):
            return _map.get('class')

        return None
