from typing import List

from pydantic import BaseModel


class AccountBalanceResponseItem(BaseModel):
    accountAlias: str
    asset: str
    balance: str
    crossWalletBalance: str
    crossUnPnl: str
    availableBalance: str
    maxWithdrawAmount: str
    marginAvailable: bool
    updateTime: int


class AccountBalanceResponse(BaseModel):
    data: List[AccountBalanceResponseItem]
