from pydantic import BaseModel


class OrderSLTP(BaseModel):
    order_id: str
    order_type: str
    order_status: str
    external_id: str
    quantity: float
    price: float
    order_trade_time: str
    
