from metastock.modules.mbinance.um.api_schema.event.kline_event import KlineData
from metastock.modules.mbinance.um.api_schema.response.candless_tick import Candlestick
from metastock.modules.mbinance.value.common import TimeInterval


def kline_to_candlestick(kline: KlineData) -> Candlestick:
    # Sử dụng tên trường Python chính xác từ model KlineData
    return Candlestick(
        open_time=kline.open_time,
        open=kline.open,
        high=kline.high,
        low=kline.low,
        close=kline.close,
        volume=kline.volume,
        close_time=kline.close_time,
        quote_asset_volume=kline.quote_asset_volume,
        number_of_trades=kline.number_of_trades,
        taker_buy_volume=kline.taker_buy_volume,
        taker_buy_quote_asset_volume=kline.taker_buy_quote_asset_volume,
        ignore=kline.ignore,
    )


def candlestick_to_kline(
    candlestick: Candlestick,
    is_closed: bool = True,
    interval: TimeInterval = TimeInterval.ONE_MINUTE.value,
) -> KlineData:
    # Sử dụng tên trường Python chính xác từ model Candlestick và giả định cho interval
    return KlineData(
        t=candlestick.open_time,
        T=candlestick.close_time,
        i=interval,
        f=None,
        L=None,
        o=candlestick.open,
        c=candlestick.close,
        h=candlestick.high,
        l=candlestick.low,
        v=candlestick.volume,
        n=candlestick.number_of_trades,
        x=is_closed,  # Trust at not closed
        q=candlestick.quote_asset_volume,
        V=candlestick.taker_buy_volume,
        Q=candlestick.taker_buy_quote_asset_volume,
        B=candlestick.ignore,
    )
