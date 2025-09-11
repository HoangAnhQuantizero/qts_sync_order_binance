from app.constants import EventOrderUpdate
from app.entities.order_sltp import OrderSLTP
from app.entities.order_core import OrderCore
from app.entities.kafka_response import KafkaResponse
from app.kafka_producer import KafkaProducerService
from app.core.config import settings
from loguru import logger


def new_order_handler(message: dict) -> KafkaResponse:
    kafka_producer = KafkaProducerService(settings.KAFKA_BOOTSTRAP_SERVERS)
    try:
        data = message[EventOrderUpdate.ORDER_DETAILS]
        client_order_id = data[EventOrderUpdate.CLIENT_ORDER_ID]

        order_new = None

        if "_sl" in client_order_id or "_tp" in client_order_id:  
            order_new = OrderSLTP(
                order_id=str(data[EventOrderUpdate.ORDER_ID]),
                order_type=data[EventOrderUpdate.ORDER_TYPE],
                order_status="NEW",
                external_id=client_order_id,
                quantity=float(data[EventOrderUpdate.ORIGINAL_QUANTITY]),
                price=float(data[EventOrderUpdate.ORIGINAL_PRICE]) if data[EventOrderUpdate.ORIGINAL_PRICE] else 0.0,
                order_trade_time=str(data[EventOrderUpdate.ORDER_TRADE_TIME]),
            )
        elif "_core" in client_order_id:
            order_new = OrderCore(
                symbol=data[EventOrderUpdate.SYMBOL],
                side=data[EventOrderUpdate.SIDE],
                order_type=data[EventOrderUpdate.ORDER_TYPE],
                price=float(data[EventOrderUpdate.ORIGINAL_PRICE]),
                order_status="NEW",
                order_id=str(data[EventOrderUpdate.ORDER_ID]),
                external_id=client_order_id,
                quantity=float(data[EventOrderUpdate.ORIGINAL_QUANTITY]),
                filled_quantity=float(data[EventOrderUpdate.LAST_FILLED_QUANTITY]),
                last_filled_price=float(data[EventOrderUpdate.LAST_FILLED_PRICE]),
                order_trade_time=str(data[EventOrderUpdate.ORDER_TRADE_TIME]),
            )
        
        if order_new:
            kafka_response = KafkaResponse(
                event="ORDER_TRADE_UPDATE",
                event_time=message[EventOrderUpdate.EVENT_TIME],
                data=order_new.model_dump()
            )

            kafka_producer.send(settings.KAFKA_TOPIC_1, kafka_response.model_dump())
            return kafka_response
        else: return None
        
    except Exception as e:
        logger.error(f"Error processing new order: {e}")
        return None
