from enum import Enum


class OrderType(Enum):
    """
    Enum representing Order Types for orders on Binance Futures.

    - `LIMIT`: Limit Order (Lệnh giới hạn).
    - `MARKET`: Market Order (Lệnh thị trường).
    - `STOP`: Stop Order (Lệnh stop).
    - `TAKE_PROFIT`: Take Profit Order (Lệnh take profit).
    - `STOP_MARKET`: Stop Market Order (Lệnh stop thị trường).
    - `TAKE_PROFIT_MARKET`: Take Profit Market Order (Lệnh take profit thị trường).
    - `TRAILING_STOP_MARKET`: Trailing Stop Market Order (Lệnh trailing stop thị trường).
    """

    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP = "STOP"
    TAKE_PROFIT = "TAKE_PROFIT"
    STOP_MARKET = "STOP_MARKET"
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"
    TRAILING_STOP_MARKET = "TRAILING_STOP_MARKET"


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderPositionSide(Enum):
    BOTH = "BOTH"
    LONG = "LONG"
    SHORT = "SHORT"


class OrderTimeInForce(Enum):
    """
    Enum representing Time In Force options for orders on Binance Futures.

    - `GTC`: Good Till Cancel (Lệnh có hiệu lực cho đến khi bị hủy).
    - `IOC`: Immediate or Cancel (Lệnh được thực hiện ngay lập tức hoặc bị hủy ngay lập tức).
    - `FOK`: Fill or Kill (Lệnh được thực hiện toàn bộ hoặc bị hủy toàn bộ).
    - `GTX`: Good Till Crossing (Post Only) (Lệnh có hiệu lực cho đến khi có lệnh khớp hoặc bị hủy).
    - `GTD`: Good Till Date (Lệnh có hiệu lực cho đến một ngày cụ thể).
    """

    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"
    GTX = "GTX"
    GTD = "GTD"


class OrderStatus(Enum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"
    EXPIRED_IN_MATCH = "EXPIRED_IN_MATCH"


class OrderWorkingType(Enum):
    """
    Enum biểu thị các tùy chọn Loại Làm việc (Working Type) cho các đơn đặt lệnh trên Binance Futures.

    - `MARK_PRICE`: Giá dừng được kích hoạt bởi Giá Đánh Giá (Mark Price).
    - `CONTRACT_PRICE`: Giá dừng được kích hoạt bởi Giá Hợp Đồng (Contract Price).
    """

    MARK_PRICE = "MARK_PRICE"
    CONTRACT_PRICE = "CONTRACT_PRICE"


class OrderPriceMatch(Enum):
    """
    Enum biểu thị tùy chọn Price Match cho các đơn đặt lệnh LIMIT/STOP/TAKE_PROFIT trên Binance Futures.

    - `NONE`: Không tự động so khớp giá.
    - `OPPONENT`: Giá tốt nhất của đối thủ.
    - `OPPONENT_5`: Giá tốt nhất thứ 5 của đối thủ.
    - `OPPONENT_10`: Giá tốt nhất thứ 10 của đối thủ.
    - `OPPONENT_20`: Giá tốt nhất thứ 20 của đối thủ.
    - `QUEUE`: Giá tốt nhất trên cùng một bên của sổ lệnh.
    - `QUEUE_5`: Giá tốt nhất thứ 5 trên cùng một bên của sổ lệnh.
    - `QUEUE_10`: Giá tốt nhất thứ 10 trên cùng một bên của sổ lệnh.
    - `QUEUE_20`: Giá tốt nhất thứ 20 trên cùng một bên của sổ lệnh.
    """

    NONE = "NONE"
    OPPONENT = "OPPONENT"
    OPPONENT_5 = "OPPONENT_5"
    OPPONENT_10 = "OPPONENT_10"
    OPPONENT_20 = "OPPONENT_20"
    QUEUE = "QUEUE"
    QUEUE_5 = "QUEUE_5"
    QUEUE_10 = "QUEUE_10"
    QUEUE_20 = "QUEUE_20"
