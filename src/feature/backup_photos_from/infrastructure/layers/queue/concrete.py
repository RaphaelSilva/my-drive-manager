
from typing import Optional

from src.feature.backup_photos_from.infrastructure.layers.queue.abstract import \
    AbstractQueueLayer
from src.feature.backup_photos_from.infrastructure.drivers.rabbitmq.adapter import \
    RabbitMQTopicClient, \
    RabbitMQTopicClientData


class QueueLayer():

    @staticmethod
    def create(queue_name: Optional[str] = None) -> AbstractQueueLayer:
        # TODO: Implement a factory to create the correct instance
        return RabbitMQTopicClient() if not queue_name else RabbitMQTopicClient(
            RabbitMQTopicClientData(
                queue_name=queue_name,
                topic_name=f"{queue_name}.topic",
                routing_key=f"{queue_name}.routing_key"
            )
        )
