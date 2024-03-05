from typing import List

from pydantic import BaseModel


class Candlestick(BaseModel):
    open_time: int
    open: str
    high: str
    low: str
    close: str
    volume: str
    close_time: int
    quote_asset_volume: str
    number_of_trades: int
    taker_buy_volume: str
    taker_buy_quote_asset_volume: str
    ignore: str


class ContinuousContractKline(BaseModel):
    data: List[Candlestick]
