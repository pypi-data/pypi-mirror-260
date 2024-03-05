from typing import List

from pydantic import BaseModel


class PositionInfo(BaseModel):
    entryPrice: str
    breakEvenPrice: str
    marginType: str
    isAutoAddMargin: bool
    isolatedMargin: str
    leverage: str
    liquidationPrice: str
    markPrice: str
    maxNotionalValue: str
    positionAmt: str
    notional: str
    isolatedWallet: str
    symbol: str
    unRealizedProfit: str
    positionSide: str
    updateTime: int


class PositionInfoResponse(BaseModel):
    data: List[PositionInfo]
