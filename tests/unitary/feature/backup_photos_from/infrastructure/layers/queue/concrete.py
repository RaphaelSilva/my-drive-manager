
from src.feature.backup_files_from.infrastructure.drivers.rabbitmq.adapter import RabbitMQTopicClient


class QueueLayer():
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.instance = RabbitMQTopicClient(queue_name)

    def __getattr__(self, attr_name):
        return self.instance.__getattribute__(attr_name)

    @staticmethod
    def create(queue_name: str):
        # TODO: Implement a factory to create the correct instance
        return RabbitMQTopicClient(queue_name)