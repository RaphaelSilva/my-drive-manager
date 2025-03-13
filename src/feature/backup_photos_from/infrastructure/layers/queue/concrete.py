
from src.feature.backup_photos_from.infrastructure.drivers.rabbitmq.adapter import RabbitMQTopicClient


class QueueLayer():
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.instance = RabbitMQTopicClient(queue_name)

    def __getattr__(self, attr_name):
        return self.instance.__getattribute__(attr_name)
