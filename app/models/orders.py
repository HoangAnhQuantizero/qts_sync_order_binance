from sqlalchemy import (
    Column, String, DateTime, Enum, ForeignKey, Numeric, JSON, func, Integer
)
from sqlalchemy.orm import relationship

from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String, nullable=False)
    order = Column(String, nullable=False)

    bot_id = Column(String, ForeignKey("bots.name"), nullable=False)
    bot = relationship("Bot", backref="orders")

    datetime = Column(DateTime, nullable=False)
    pair = Column(String, nullable=False)

    mode = Column(Enum("testing", "production", name="order_mode"), nullable=False)
    type = Column(Enum("MARKET", "LIMIT", name="order_type"), nullable=False)
    side = Column(Enum("BUY", "SELL", name="order_side"), nullable=False)

    amount = Column(Numeric(20, 8), nullable=False)
    signal_entry_price = Column(Numeric(20, 8), nullable=False)
    real_entry_price = Column(Numeric(20, 8), nullable=True)
    close_price = Column(Numeric(20, 8), nullable=True)

    sl = Column(Numeric(20, 8), nullable=True)
    tp = Column(Numeric(20, 8), nullable=True)

    leverage = Column(Integer, nullable=True)

    fee_open = Column(Numeric(20, 8), nullable=True)
    fee_close = Column(Numeric(20, 8), nullable=True)

    sl_actual = Column(Numeric(20, 8), nullable=True)
    tp_actual = Column(Numeric(20, 8), nullable=True)

    progress = Column(String, nullable=True)
    external_order_id = Column(String, nullable=True)

    status = Column(
        Enum("NEW", "CANCELED", "FILLED", "PARTIALLY_FILLED", "EXPIRED", "CLOSED", "EXPIRED_IN_MATCH",name="order_status"),
        nullable=False,
    )

    pnl = Column(Numeric(20, 8), nullable=True)

    metadata_json = Column("metadata", JSON, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

