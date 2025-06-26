from abc import ABC, abstractmethod
from typing import Optional


class AbstractQueueLayer(ABC):
    queue_name: str
    topic_name: str

    def __init__(self, queue_name: str, topic_name: str) -> None:
        self.queue_name = queue_name
        self.topic_name = topic_name

    @abstractmethod
    async def send_message(self, message: str):
        raise NotImplementedError

    @abstractmethod
    async def send_message_dlq(self, message: str):
        raise NotImplementedError

    @abstractmethod
    async def receive_message(self) -> Optional[str]:
        raise NotImplementedError
    
    @abstractmethod
    async def resolve_topic(self) -> bool:
        raise NotImplementedError
