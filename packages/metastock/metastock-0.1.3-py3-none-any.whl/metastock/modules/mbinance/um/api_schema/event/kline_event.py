from typing import Optional

from pydantic import BaseModel, Field


class KlineData(BaseModel):
    open_time: int = Field(..., alias="t")
    close_time: int = Field(..., alias="T")
    interval: Optional[str] = Field(alias="i", default=None)
    first_update_id: Optional[int] = Field(alias="f", default=None)
    last_update_id: Optional[int] = Field(alias="L", default=None)
    open: str = Field(..., alias="o")
    close: str = Field(..., alias="c")
    high: str = Field(..., alias="h")
    low: str = Field(..., alias="l")
    volume: str = Field(..., alias="v")
    number_of_trades: int = Field(..., alias="n")
    is_closed: bool = Field(..., alias="x")
    quote_asset_volume: str = Field(..., alias="q")
    taker_buy_volume: str = Field(..., alias="V")
    taker_buy_quote_asset_volume: str = Field(..., alias="Q")
    ignore: str = Field(..., alias="B")


class KlineEvent(BaseModel):
    e: str
    E: int
    ps: str
    ct: str
    k: KlineData
