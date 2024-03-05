from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EventReasonType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    ORDER = "ORDER"
    FUNDING_FEE = "FUNDING_FEE"
    WITHDRAW_REJECT = "WITHDRAW_REJECT"
    ADJUSTMENT = "ADJUSTMENT"
    INSURANCE_CLEAR = "INSURANCE_CLEAR"
    ADMIN_DEPOSIT = "ADMIN_DEPOSIT"
    ADMIN_WITHDRAW = "ADMIN_WITHDRAW"
    MARGIN_TRANSFER = "MARGIN_TRANSFER"
    MARGIN_TYPE_CHANGE = "MARGIN_TYPE_CHANGE"
    ASSET_TRANSFER = "ASSET_TRANSFER"
    OPTIONS_PREMIUM_FEE = "OPTIONS_PREMIUM_FEE"
    OPTIONS_SETTLE_PROFIT = "OPTIONS_SETTLE_PROFIT"
    AUTO_EXCHANGE = "AUTO_EXCHANGE"
    COIN_SWAP_DEPOSIT = "COIN_SWAP_DEPOSIT"
    COIN_SWAP_WITHDRAW = "COIN_SWAP_WITHDRAW"


class AccountBalanceItem(BaseModel):
    asset: str = Field(alias="a")  # Alias for Asset
    wallet_balance: str = Field(alias="wb")  # Alias for Wallet Balance
    cross_wallet_balance: str = Field(alias="cw")  # Alias for Cross Wallet Balance
    balance_change: str = Field(
        alias="bc"
    )  # Alias for Balance Change except PnL and Commission


class PositionItem(BaseModel):
    symbol: str = Field(alias="s")  # Alias for Symbol
    position_amount: str = Field(alias="pa")  # Alias for Position Amount
    entry_price: str = Field(alias="ep")  # Alias for Entry Price
    breakeven_price: str = Field(alias="bep")  # Alias for Breakeven Price
    accumulated_realized: str = Field(
        alias="cr"
    )  # Alias for Accumulated Realized (Pre-fee)
    unrealized_pnl: str = Field(alias="up")  # Alias for Unrealized PnL
    margin_type: str = Field(alias="mt")  # Alias for Margin Type
    isolated_wallet: str = Field(
        alias="iw"
    )  # Alias for Isolated Wallet (if isolated position)
    position_side: str = Field(alias="ps")  # Alias for Position Side


class AccountUpdateData(BaseModel):
    event_reason_type: EventReasonType = Field(
        alias="m", description="Event reason type"
    )
    balances: list[AccountBalanceItem] = Field(alias="B")  # Alias for List of Balances
    positions: Optional[list[PositionItem]] = Field(
        alias="P"
    )  # Alias for List of Position Items


class AccountUpdateEvent(BaseModel):
    event_type: str = Field(alias="e")  # Alias for Event Type
    event_time: int = Field(alias="E")  # Alias for Event Time
    transaction: int = Field(alias="T")  # Alias for Transaction
    update_data: AccountUpdateData = Field(alias="a")  # Alias for Update Data
