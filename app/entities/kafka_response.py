from pydantic import BaseModel
from typing import Any, Dict


class KafkaResponse(BaseModel):
    event: str
    event_time: int
    data: Dict[str, Any]
