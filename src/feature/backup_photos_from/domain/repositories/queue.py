from src.feature.backup_photos_from.infrastructure.layers.queue.abstract import AbstractQueueLayer


class QueueRepository:
    def __init__(self, queue_layer: AbstractQueueLayer):
        self.queue = queue_layer

    def put(self, file: dict) -> None:
        self.queue.send_message(file)

    def get(self) -> dict:
        return self.queue.receive_messages()

    def empty(self) -> bool:
        return self.queue.is_empty()

    def size(self) -> int:
        return self.queue.size()

    def dlq(self, message: dict, error: Exception) -> None:
        message["error"] = error.__dict__
        self.queue.send_message_dlq(message)
