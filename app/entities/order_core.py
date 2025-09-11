

from pydantic import BaseModel

class OrderCore(BaseModel):
    symbol: str
    side: str
    order_type: str
    price: float
    order_status: str
    order_id: str
    external_id: str
    quantity: float
    filled_quantity: float
    last_filled_price: float
    order_trade_time: str
    