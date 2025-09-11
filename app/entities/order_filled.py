

from pydantic import BaseModel


class OrderFilled(BaseModel):
    order_type: str
    order_id: str
    order_status: str
    signal_entry_price: float
    real_entry_price: float
    external_id: str
    filled_quantity: float
    quantity: float
    fee: float
    order_trade_time: str