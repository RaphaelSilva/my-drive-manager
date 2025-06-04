import os  # Import the 'os' module

from src.feature.backup_photos_from.infrastructure.drivers.rabbitmq.base import RabbitMQBaseClient
from src.feature.backup_photos_from.infrastructure.layers.queue.abstract import AbstractQueueLayer
from src.shared.infrastructure.logging.syslog import logger


class RabbitMQTopicClient(AbstractQueueLayer, RabbitMQBaseClient):
    def __init__(self, queue_name: str = None) -> None:
        super().__init__(queue_name)
        self.topic_name = os.environ.get("RABBITMQ_TOPIC_NAME")
        self.routing_key = os.environ.get("RABBITMQ_ROUTING_KEY")

    async def send_message(self, message: str):
        await self.create_message(self.topic_name, self.routing_key, message)
        logger.info(
            "Message sent to RabbitMQ",
            extra={"body": message},
        )

    async def send_message_dlq(self, message: str):
        topic_name = f'{self.topic_name}.dlq'
        await self.create_message(topic_name, self.routing_key, message)
        logger.info(
            "Message sent to RabbitMQ DLQ",
            extra={"body": message},
        )

    async def receive_message(self) -> str:
        response = await self.read_message(self.topic_name)
        return response['body']
