from metastock.modules.core.util.registry import registry


class UMValue(object):
    PAIR_KEY = "UM_PAIR"
    CONTRACT_TYPE = "PERPETUAL"

    ROUND_DECIMAL = 4

    @classmethod
    def HULL_LENGTH(cls):
        value = registry.get_data("UM_HULL_LENGTH")
        return value if value else 10

    @classmethod
    def SET_HULL_LENGTH(cls, value: int):
        registry.set_data("UM_HULL_LENGTH", value)

    @classmethod
    def WT_N1(cls):
        value = registry.get_data("UM_WT_N1")
        return value if value else 12

    @classmethod
    def WT_N2(cls):
        value = registry.get_data("UM_WT_N1")
        return value if value else 24

    @classmethod
    def set_PAIR(cls, pair: str):
        registry.set_data(UMValue.PAIR_KEY, pair)

    @classmethod
    def PAIR(cls):
        value = registry.get_data(UMValue.PAIR_KEY)
        if value is None:
            raise ValueError("Please configure symbol into registry")

        return value

    @classmethod
    def SYMBOL(cls):
        value = registry.get_data(UMValue.PAIR_KEY)
        if value is None:
            raise ValueError("Please configure symbol into registry")

        return value
