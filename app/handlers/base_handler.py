from loguru import logger
from app.constants import *
from app.handlers.cancel_order_handler import cancel_order_handler
from app.handlers.filled_order_handler import filled_order_handler
from app.handlers.new_order_handler import new_order_handler

class BaseHandler:
    def handle_message(self, message: dict):
        message_type = message.get("e")
        if message_type == "ORDER_TRADE_UPDATE":
            order_details = message[EventOrderUpdate.ORDER_DETAILS]
            order_status = order_details[EventOrderUpdate.ORDER_STATUS]
            
            if order_status == "NEW":
                new_order_handler(message)
            elif order_status == "CANCELED":
                cancel_order_handler(message)
            elif order_status == "FILLED":
                filled_order_handler(message)   
            elif order_status == "REJECTED":
                logger.info(f"🚫 Order rejected: {order_details[EventOrderUpdate.CLIENT_ORDER_ID]}")
            