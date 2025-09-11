from pydantic import BaseModel


class OrderCancel(BaseModel):
    order_type: str
    order_id: str
    order_status: str
    external_id: str
    order_trade_time: str