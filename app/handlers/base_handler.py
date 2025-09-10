from loguru import logger
from app.constants import *
from app.handlers.filled_message_handler import FilledMessageHandler
from app.handlers.new_message_handler import NewMessageHandler

class BaseHandler:
    def handle_message(self, message: dict):
        message_type = message.get("e")
        if message_type == "ORDER_TRADE_UPDATE":
            order_details = message[EventOrderUpdate.ORDER_DETAILS]
            order_status = order_details[EventOrderUpdate.ORDER_STATUS]
            
            if order_status == "NEW":
                NewMessageHandler().handle_message(message)
            elif order_status == "CANCELED":
                logger.info(f"Order canceled: {message}")
            elif order_status == "FILLED":
                FilledMessageHandler().handle_message(message)
            elif order_status == "REJECTED":
                logger.info(f"Order rejected: {message}")
            