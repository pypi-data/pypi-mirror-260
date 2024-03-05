from binance.um_futures import UMFutures

from metastock.modules.core.util.environment import env
from metastock.modules.mbinance.error.fatal_error import FatalError
from metastock.modules.mbinance.util.is_testnet import is_testnet
from metastock.modules.mbinance.value.common import CommonValue

um_futures_client = None


def get_um_client() -> UMFutures:
    global um_futures_client
    if um_futures_client is None:
        api_key = env().get("API_KEY")
        api_secret = env().get("API_SECRET")
        if not api_key:
            raise FatalError("API_KEY environment variable is not set")

        if not api_secret:
            raise FatalError("API_SECRET environment variable is not set")

        um_futures_client = (
            UMFutures(
                key=api_key,
                secret=api_secret,
                base_url=CommonValue.API_TESTNET_URL,
            )
            if is_testnet()
            else UMFutures(
                key=api_key,
                secret=api_secret,
            )
        )

    return um_futures_client
