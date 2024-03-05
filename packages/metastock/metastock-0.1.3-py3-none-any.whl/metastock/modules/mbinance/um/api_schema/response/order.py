from typing import Optional

from pydantic import BaseModel, Extra, Field


class OrderResponse(BaseModel):
    client_order_id: str = Field(alias="clientOrderId")
    cumulative_quantity: Optional[str] = Field(alias="cumQty", default=None)
    cumulative_quote: str = Field(alias="cumQuote")
    executed_quantity: str = Field(alias="executedQty")
    order_id: int = Field(alias="orderId")
    average_price: str = Field(alias="avgPrice")
    original_quantity: str = Field(alias="origQty")
    price: str
    reduce_only: bool = Field(alias="reduceOnly")
    side: str
    position_side: str = Field(alias="positionSide")
    status: str
    stop_price: Optional[str] = Field(
        alias="stopPrice", description=None
    )  # Ignore when order type is TRAILING_STOP_MARKET
    close_position: bool = Field(
        alias="closePosition", description=None
    )  # If Close-All
    symbol: str
    time_in_force: str = Field(alias="timeInForce")
    type: str
    original_type: str = Field(alias="origType")
    activation_price: Optional[str] = Field(
        alias="activatePrice", description=None, default=None
    )  # Only return with TRAILING_STOP_MARKET order
    price_rate: Optional[str] = Field(
        alias="priceRate", description=None, default=None
    )  # Only return with TRAILING_STOP_MARKET order
    update_time: int = Field(alias="updateTime")
    working_type: str = Field(alias="workingType")
    price_protect: Optional[bool] = Field(
        alias="priceProtect"
    )  # If conditional order trigger is protected
    price_match_mode: str = Field(alias="priceMatch")
    self_trade_prevention_mode: str = Field(alias="selfTradePreventionMode")
    good_till_date: int = Field(alias="goodTillDate")

    class Config:
        extra = Extra.ignore  # Bỏ qua các trường thừa
