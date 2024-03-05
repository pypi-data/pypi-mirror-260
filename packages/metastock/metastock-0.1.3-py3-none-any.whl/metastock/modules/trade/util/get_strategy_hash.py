from metastock.modules.core.util.hash_string_md5 import hash_string_md5


def get_strategy_hash(strategy_name: str, strategy_input: dict, from_date: str, to_date: str):
    return hash_string_md5(strategy_name + str(strategy_input) + from_date + to_date)
