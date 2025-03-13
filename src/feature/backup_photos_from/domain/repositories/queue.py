from src.feature.backup_photos_from.infrastructure.layers.queue.abstract import AbstractQueueLayer

class QueueRepository:
    def __init__(self, queue_layer: AbstractQueueLayer):
        self.queue = queue_layer

    def put(self, file: dict) -> None:
        self.queue.send_message(file)
