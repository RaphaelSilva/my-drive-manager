from src.feature.backup_photos_from.infrastructure.drivers.rabbitmq.adapter import RabbitMQClient
from src.feature.backup_photos_from.infrastructure.factories.queue.abstract import AbstractQueueLayer


def queue_factory(queue_name: str) -> AbstractQueueLayer:
    """Factory function for creating a queue layer."""
    # This is a placeholder for a real factory function
    return RabbitMQClient(queue_name)
