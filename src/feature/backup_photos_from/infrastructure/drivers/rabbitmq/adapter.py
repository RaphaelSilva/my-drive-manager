import os

from src.feature.backup_photos_from.infrastructure.drivers.rabbitmq.base import RabbitMQBaseClient
from src.feature.backup_photos_from.infrastructure.layers.queue.abstract import AbstractQueueLayer
from src.shared.infrastructure.logging.syslog import logger


class RabbitMQTopicClient(AbstractQueueLayer, RabbitMQBaseClient):
    def __init__(self, queue_name: str = None) -> None:
        super().__init__(queue_name)
        self.topic_name = os.getenv("RABBITMQ_TOPIC_NAME")
        self.routing_key = os.getenv("RABBITMQ_ROUTING_KEY")

    async def send_message(self, message: str):
        response = await self.create_message(self.topic_name, self.routing_key, message)
        logger.info(
            "Message sent to RabbitMQ",
            extra={"message": message, "response": response},
        )

    async def receive_messages(self, max_messages: int) -> list[str]:
        raise NotImplementedError

    async def delete_message(self, receipt_handle: str):
        raise NotImplementedError

    async def send_message_dlq(self, message: str):
        raise NotImplementedError
