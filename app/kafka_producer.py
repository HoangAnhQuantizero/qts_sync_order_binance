import json
from kafka import KafkaProducer
from loguru import logger

class KafkaProducerService:
    def __init__(self, bootstrap_servers: str):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    def send(self, topic: str, message: dict) -> bool:
        try:
            self.producer.send(topic, value=message).get(timeout=10)
            logger.info(f"✅ Sent to {topic}: {message}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send to {topic}: {e}")
            return False

    def close(self):
        self.producer.close()

if __name__ == "__main__":
    producer = KafkaProducerService("localhost:9092")
    producer.send("test-topic", {"hello": "world"})
    producer.close()

