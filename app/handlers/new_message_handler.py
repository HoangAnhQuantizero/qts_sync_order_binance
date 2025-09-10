from loguru import logger
from app.constants import EventOrderUpdate


class NewMessageHandler:
    def handle_message(self, message: dict):
        order_details = message[EventOrderUpdate.ORDER_DETAILS]
        client_order_id = order_details[EventOrderUpdate.CLIENT_ORDER_ID]
        order_id = order_details[EventOrderUpdate.ORDER_ID]

        logger.debug(f"New order , client_order_id: {client_order_id}, order_id: {order_id}")