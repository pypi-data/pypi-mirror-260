from typing import Optional

from pydantic import BaseModel, Field


class OrderTradeUpdateInfo(BaseModel):
    # Tên của cặp tiền tệ (ví dụ: BTCUSDT) |
    symbol: str = Field(alias="s")

    # ID đơn hàng do khách hàng cung cấp |
    client_order_id: str = Field(alias="c")

    # Hướng của đơn hàng (MUA/SELL) |
    side: str = Field(alias="S")

    # Loại đơn hàng (ví dụ: LIMIT, MARKET) |
    order_type: str = Field(alias="o")

    # Thời gian tồn tại của đơn hàng (ví dụ: GTC - Good Till Cancelled) |
    time_in_force: str = Field(alias="f")

    # Số lượng gốc của đơn hàng |
    original_quantity: float = Field(alias="q")

    # Giá gốc của đơn hàng
    original_price: float = Field(alias="p")

    # Giá trung bình mà đơn hàng đã được thực hiện |
    average_price: float = Field(alias="ap")

    # Giá dừng cho đơn hàng dừng (Stop Order) |
    stop_price: float = Field(alias="sp")

    # Loại thực thi của đơn hàng (ví dụ: NEW, FILLED)
    execution_type: str = Field(alias="x")

    # Trạng thái của đơn hàng (ví dụ: NEW, PARTIALLY_FILLED) |
    order_status: str = Field(alias="X")

    # ID đơn hàng trên hệ thống |
    order_id: int = Field(alias="i")

    # Số lượng đã được điền vào lần cuối của đơn hàng
    last_filled_quantity: float = Field(alias="l")

    # Tổng số lượng đã được điền vào của đơn hàng
    filled_accumulated_quantity: float = Field(alias="z")

    # Giá của lần điền vào cuối cùng
    last_filled_price: float = Field(alias="L")

    # Tài sản được sử dụng để trả hoa hồng
    commission_asset: str = Field(alias="N", default=None)

    # Số lượng hoa hồng
    commission: float = Field(alias="n", default=None)

    # Thời gian thực hiện giao dịch của đơn hàng
    order_trade_time: int = Field(alias="T")

    # ID của giao dịch
    trade_id: int = Field(alias="t")

    # Tổng giá trị đặt mua
    bids_notional: float = Field(alias="b")

    # Tổng giá trị đặt bán
    asks_notional: float = Field(alias="a")

    # Đánh dấu đơn hàng là tạo lập thị trường (maker) hay không
    is_maker: bool = Field(alias="m")

    # Đánh dấu đơn hàng chỉ giảm vị thế
    is_reduce_only: bool = Field(alias="R")

    # Loại giá dừng (ví dụ: CONTRACT_PRICE)
    stop_price_working_type: str = Field(alias="wt")

    # Loại đơn hàng gốc
    original_order_type: str = Field(alias="ot")

    # Vị thế của đơn hàng (LONG/SHORT)
    position_side: str = Field(alias="ps")

    # Đánh dấu đơn hàng là đóng tất cả vị thế
    is_close_all: bool = Field(alias="cp")

    # Giá kích hoạt cho đơn hàng dừng theo dõi (Trailing Stop Order)
    activation_price: Optional[float] = Field(alias="AP", default=None)

    # Tỷ lệ gọi lại cho đơn hàng dừng theo dõi
    callback_rate: Optional[float] = Field(alias="cr", default=None)

    # Đánh dấu bảo vệ giá đã được bật
    is_price_protection: bool = Field(alias="pP")

    # Lợi nhuận thực hiện của giao dịch
    realized_profit: float = Field(alias="rp")

    # Chế độ STP (Self-Trade Prevention)
    stp_mode: str = Field(alias="V")

    # Chế độ khớp giá (ví dụ: OPPONENT)
    price_match_mode: str = Field(alias="pm")

    # Thời gian tự động hủy đơn hàng GTD (Good Till Date)
    gtd_order_auto_cancel_time: int = Field(alias="gtd")

    class Config:
        extra = "allow"  # Cho phép các trường khác thừa
        populate_by_name = True


class OrderTradeUpdateEvent(BaseModel):
    event_type: str = Field(alias="e")
    event_time: int = Field(alias="E")
    transaction_time: int = Field(alias="T")
    order_info: OrderTradeUpdateInfo = Field(alias="o")
