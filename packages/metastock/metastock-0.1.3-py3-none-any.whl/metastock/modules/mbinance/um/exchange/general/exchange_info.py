from metastock.modules.mbinance.um.util.get_client import get_um_client


def get_exchange_info() -> dict:
    um_futures_client = get_um_client()
    data = um_futures_client.exchange_info()

    return data
