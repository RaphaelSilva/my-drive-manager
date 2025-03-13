from abc import ABC, abstractmethod


class AbstractQueueLayer(ABC):
    def __init__(self, queue_name: str):
        self.queue_name = queue_name

    @abstractmethod
    def send_message(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def receive_messages(self, max_messages: int) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def delete_message(self, receipt_handle: str):
        raise NotImplementedError

    @abstractmethod
    def send_message_dlq(self, message: str):
        raise NotImplementedError
