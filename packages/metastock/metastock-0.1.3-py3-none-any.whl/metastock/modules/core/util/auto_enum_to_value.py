from enum import Enum
from functools import wraps


def auto_enum_to_value(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        new_kwargs = {
            k: v.value if isinstance(v, Enum) else v for k, v in kwargs.items()
        }
        return func(*args, **new_kwargs)

    return wrapper
