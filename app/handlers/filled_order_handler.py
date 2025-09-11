from app.constants import EventOrderUpdate
from app.entities.order_filled import OrderFilled
from app.entities.kafka_response import KafkaResponse
from app.kafka_producer import KafkaProducerService
from app.core.config import settings
from loguru import logger


def filled_order_handler(message: dict) -> KafkaResponse:
    kafka_producer = KafkaProducerService(settings.KAFKA_BOOTSTRAP_SERVERS)
    try:
        data = message[EventOrderUpdate.ORDER_DETAILS]
        order_filled = None

        if "_core" in data[EventOrderUpdate.CLIENT_ORDER_ID]:        
            order_filled = OrderFilled(
                order_type=data[EventOrderUpdate.ORDER_TYPE],
                order_id=str(data[EventOrderUpdate.ORDER_ID]),
                order_status="FILLED",
                signal_entry_price=float(data[EventOrderUpdate.ORIGINAL_PRICE]),
                real_entry_price=float(data[EventOrderUpdate.LAST_FILLED_PRICE]),
                external_id=data[EventOrderUpdate.CLIENT_ORDER_ID],
                filled_quantity=float(data[EventOrderUpdate.LAST_FILLED_QUANTITY]),
                quantity=float(data[EventOrderUpdate.ORIGINAL_QUANTITY]),
                fee=float(data[EventOrderUpdate.COMMISSION]),
                order_trade_time=str(data[EventOrderUpdate.ORDER_TRADE_TIME]),
            )
        elif "_sl" in data[EventOrderUpdate.CLIENT_ORDER_ID] or "_tp" in data[EventOrderUpdate.CLIENT_ORDER_ID]:
            order_filled = OrderFilled(
                order_type=data[EventOrderUpdate.ORDER_TYPE],
                order_id=str(data[EventOrderUpdate.ORDER_ID]),
                order_status="FILLED",
                signal_entry_price=float(data[EventOrderUpdate.ORIGINAL_PRICE]),
                real_entry_price=float(data[EventOrderUpdate.LAST_FILLED_PRICE]),
                external_id=data[EventOrderUpdate.CLIENT_ORDER_ID],
                filled_quantity=float(data[EventOrderUpdate.LAST_FILLED_QUANTITY]),
                quantity=float(data[EventOrderUpdate.ORIGINAL_QUANTITY]),
                fee=float(data[EventOrderUpdate.COMMISSION]),
                order_trade_time=str(data[EventOrderUpdate.ORDER_TRADE_TIME]),
            )

        if order_filled:
            kafka_response = KafkaResponse(
                event="ORDER_TRADE_UPDATE",
                event_time=message[EventOrderUpdate.EVENT_TIME],
                data=order_filled.model_dump()
            )
            kafka_producer.send(settings.KAFKA_TOPIC_1, kafka_response.model_dump())
            return kafka_response
        else: return None
        
    except Exception as e:
        logger.error(f"Error processing filled order: {e}")
        return None
    