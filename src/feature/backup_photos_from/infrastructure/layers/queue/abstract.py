from abc import ABC, abstractmethod


class AbstractQueueLayer(ABC):
    def __init__(self, queue_name: str):
        self.queue_name = queue_name

    @abstractmethod
    async def send_message(self, message: str):
        raise NotImplementedError

    @abstractmethod
    async def send_message_dlq(self, message: str):
        raise NotImplementedError

    @abstractmethod
    async def receive_message(self) -> str:
        raise NotImplementedError
