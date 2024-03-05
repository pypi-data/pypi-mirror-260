from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    Float,
    Boolean,
    DateTime,
    func,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base

from metastock.modules.core.logging.logger import Logger
from metastock.modules.mbinance.um.api_schema.response.aggregate_trade_list import (
    BinanceTradeData,
)
from metastock.modules.mbinance.um.api_schema.response.candless_tick import (
    Candlestick as CandlestickResponse,
)

# Tạo bảng Candlestick nếu chưa tồn tại
Base = declarative_base()


class Candlestick(Base):
    __tablename__ = "candlesticks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String)
    interval = Column(String(3))
    open_time = Column(BigInteger, index=True)  # Thêm index cho tìm kiếm nhanh
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    close_time = Column(BigInteger)
    quote_asset_volume = Column(Float)
    number_of_trades = Column(Integer)
    taker_buy_volume = Column(Float)
    taker_buy_quote_asset_volume = Column(Float)

    __table_args__ = (
        UniqueConstraint(
            "symbol", "open_time", "interval", name="unique_symbol_open_time_interval"
        ),
    )

    def __init__(
        self,
        symbol,
        interval,
        open_time,
        open,
        high,
        low,
        close,
        volume,
        close_time,
        quote_asset_volume,
        number_of_trades,
        taker_buy_volume,
        taker_buy_quote_asset_volume,
    ):
        self.symbol = symbol
        self.interval = interval
        self.open_time = open_time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.close_time = close_time
        self.quote_asset_volume = quote_asset_volume
        self.number_of_trades = number_of_trades
        self.taker_buy_volume = taker_buy_volume
        self.taker_buy_quote_asset_volume = taker_buy_quote_asset_volume

    def __repr__(self):
        return f"<Candlestick(symbol={self.symbol}, interval={self.interval}, open_time={self.open_time}, close_time={self.close_time})>"

    @staticmethod
    def map_from_pydantic(
        symbol: str, interval: str, candlestick_data: CandlestickResponse
    ):
        try:
            return Candlestick(
                symbol=symbol,
                interval=interval,
                open_time=candlestick_data.open_time,
                open=float(candlestick_data.open),
                high=float(candlestick_data.high),
                low=float(candlestick_data.low),
                close=float(candlestick_data.close),
                volume=float(candlestick_data.volume),
                close_time=candlestick_data.close_time,
                quote_asset_volume=float(candlestick_data.quote_asset_volume),
                number_of_trades=candlestick_data.number_of_trades,
                taker_buy_volume=float(candlestick_data.taker_buy_volume),
                taker_buy_quote_asset_volume=float(
                    candlestick_data.taker_buy_quote_asset_volume
                ),
                # ignore=float(candlestick_data.ignore),
            )
        except Exception as e:
            # Xử lý lỗi nếu cần
            Logger(f"Error mapping Pydantic object to SQLAlchemy model: {e}")
            return None


class BinanceTrade(Base):
    __tablename__ = "um_aggregate_trades"

    aggregate_trade_id = Column(BigInteger, primary_key=True)
    price = Column(Float)
    quantity = Column(Float)
    first_trade_id = Column(BigInteger)
    last_trade_id = Column(BigInteger)
    timestamp = Column(BigInteger)
    was_buyer_maker = Column(Boolean)

    def __init__(
        self,
        aggregate_trade_id,
        price,
        quantity,
        first_trade_id,
        last_trade_id,
        timestamp,
        was_buyer_maker,
    ):
        self.timestamp = timestamp
        self.aggregate_trade_id = aggregate_trade_id
        self.price = price
        self.quantity = quantity
        self.first_trade_id = first_trade_id
        self.last_trade_id = last_trade_id
        self.was_buyer_maker = was_buyer_maker

    def __repr__(self):
        return f"<BinanceTrade(timestamp={self.timestamp}, price={self.price}, quantity={self.quantity}, buyer_maker={self.was_buyer_maker})>"

    @staticmethod
    def map_from_pydantic(binace_trade_data: BinanceTradeData, raise_exception=True):
        try:
            return BinanceTrade(
                timestamp=binace_trade_data.T,
                aggregate_trade_id=binace_trade_data.a,
                price=float(binace_trade_data.p),
                quantity=float(binace_trade_data.q),
                first_trade_id=binace_trade_data.f,
                last_trade_id=binace_trade_data.l,
                was_buyer_maker=binace_trade_data.m,
            )
        except Exception as e:
            # Xử lý lỗi nếu cần
            Logger(f"Error mapping Pydantic object to SQLAlchemy model: {e}")

            if raise_exception:
                raise e
            else:
                return None


class HistoryDataFetcherState(Base):
    __tablename__ = "history_data_fetcher_state"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)
    start_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger, nullable=True)
    number_of_try = Column(Integer, nullable=False)
    last_error = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())

    def __init__(self, type, start_time, end_time, number_of_try, last_error):
        self.type = type
        self.start_time = start_time
        self.end_time = end_time
        self.number_of_try = number_of_try
        self.last_error = last_error
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f"<HistoryDataFetcherState(id={self.id}, type='{self.type}', start_time={self.start_time}, end_time={self.end_time}, number_of_try={self.number_of_try}, last_error='{self.last_error}')>"
