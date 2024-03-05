from metastock.modules.mbinance.value.common import TimeInterval


def is_value_in_time_interval(value):
    return any(value == item.value for item in TimeInterval)
