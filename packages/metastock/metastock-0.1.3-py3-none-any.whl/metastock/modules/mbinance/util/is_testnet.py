from metastock.modules.core.util.environment import env

_testnet = None


def is_testnet():
    global _testnet
    if _testnet is None:
        _testnet = env().get("LIVE") != "true"

    return _testnet
