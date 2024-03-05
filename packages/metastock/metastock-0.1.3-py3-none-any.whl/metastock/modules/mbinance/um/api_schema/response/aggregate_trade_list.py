from typing import List

from pydantic import BaseModel


class BinanceTradeData(BaseModel):
    a: int  # Aggregate tradeId
    p: str  # Price
    q: str  # Quantity
    f: int  # First tradeId
    l: int  # Last tradeId
    T: int  # Timestamp
    m: bool  # Was the buyer the maker?


class AggregateTradeList(BaseModel):
    data: List[BinanceTradeData]
