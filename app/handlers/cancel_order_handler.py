from app.constants import EventOrderUpdate
from app.entities.order_cancel import OrderCancel
from app.entities.kafka_response import KafkaResponse
from app.kafka_producer import KafkaProducerService
from app.core.config import settings
from loguru import logger


def cancel_order_handler(message: dict) -> KafkaResponse:
    kafka_producer = KafkaProducerService(settings.KAFKA_BOOTSTRAP_SERVERS)
    try:
        data = message[EventOrderUpdate.ORDER_DETAILS]
        order_canceled = None

        if "_core" in data[EventOrderUpdate.CLIENT_ORDER_ID]:
            order_canceled = OrderCancel(
                order_type=data[EventOrderUpdate.ORDER_TYPE],
                order_id=str(data[EventOrderUpdate.ORDER_ID]),
                order_status="CANCELED",
                external_id=data[EventOrderUpdate.CLIENT_ORDER_ID],
                order_trade_time=str(data[EventOrderUpdate.ORDER_TRADE_TIME]),
            )

            kafka_response = KafkaResponse(
                event="ORDER_TRADE_UPDATE",
                event_time=message[EventOrderUpdate.EVENT_TIME],
                data=order_canceled.model_dump()
            )
            kafka_producer.send(settings.KAFKA_TOPIC_1, kafka_response.model_dump())
            return kafka_response
        else: return None

    except Exception as e:
        logger.error(f"Error processing cancel order: {e}")
        return None 