from loguru import logger
from app.constants import EventOrderUpdate


class FilledMessageHandler:
    def handle_message(self, message: dict):
        data = message[EventOrderUpdate.ORDER_DETAILS]
        last_filled_price = data[EventOrderUpdate.LAST_FILLED_PRICE]
        client_order_id = data[EventOrderUpdate.CLIENT_ORDER_ID]
        fee = data[EventOrderUpdate.COMMISSION]
        order_type = data[EventOrderUpdate.ORDER_TYPE]
        order_id = data[EventOrderUpdate.ORDER_ID]
        signal_entry_price = data[EventOrderUpdate.ORIGINAL_PRICE]
        quantity = data[EventOrderUpdate.ORIGINAL_QUANTITY]
        filled_quantity = data[EventOrderUpdate.LAST_FILLED_QUANTITY]

        params = {
            "event": "ORDER_TRADE_UPDATE",
            "event_time": message[EventOrderUpdate.EVENT_TIME], 
            "data": {
                "order_type": order_type,
                "order_id": str(order_id),
                "order_status": "FILLED",
                "signal_entry_price": float(signal_entry_price),
                "real_entry_price": float(last_filled_price),
                "external_id": client_order_id,
                "filled_quantity": filled_quantity,
                "quantity": float(quantity),
                "fee": fee,
                "order_trade_time": data[EventOrderUpdate.ORDER_TRADE_TIME],    
            }
        }

        logger.debug(f"Filled order , params: {params}")
