import os
from typing import Optional  # Import the 'os' module

from src.feature.backup_photos_from.infrastructure.drivers.rabbitmq.base import RabbitMQBaseClient, RabbitMQBaseClientData
from src.feature.backup_photos_from.infrastructure.layers.queue.abstract import AbstractQueueLayer
from src.shared.infrastructure.logging.syslog import logger

DEFAULT_QUEUE_NAME = "default_queue_name"
DEFAULT_TOPIC_NAME = "default_topic_name"
DEFAULT_ROUTING_KEY = "default_routing_key"


class RabbitMQTopicClientData(RabbitMQBaseClientData):
    queue_name: Optional[str] = os.environ.get(
        "RABBITMQ_QUEUE_NAME", DEFAULT_QUEUE_NAME)
    topic_name: Optional[str] = os.environ.get(
        "RABBITMQ_TOPIC_NAME", DEFAULT_TOPIC_NAME)
    routing_key: Optional[str] = os.environ.get(
        "RABBITMQ_ROUTING_KEY",  DEFAULT_ROUTING_KEY)


class RabbitMQTopicClient(AbstractQueueLayer, RabbitMQBaseClient):

    def __init__(self, data: Optional[RabbitMQTopicClientData] = None) -> None:
        AbstractQueueLayer.__init__(self,
                                    data.queue_name if data and data.queue_name else DEFAULT_QUEUE_NAME,
                                    data.topic_name if data and data.topic_name else DEFAULT_TOPIC_NAME
                                    )
        RabbitMQBaseClient.__init__(self, data)
        self.routing_key = data.routing_key if data and data.routing_key else DEFAULT_ROUTING_KEY


    async def send_message(self, message: str):
        response = await self.create_message(self.topic_name, self.routing_key, message)
        confirmation = response.get('confirmation', None)
        logger.info(
            "Message sent to RabbitMQ %s", confirmation,
            extra={
                "body": message,
                "response": response
            },
        )

    async def send_message_dlq(self, message: str):
        topic_name = f'{self.topic_name}.dlq'
        await self.create_message(topic_name, self.routing_key, message)
        logger.info(
            "Message sent to RabbitMQ DLQ",
            extra={"body": message},
        )

    async def receive_message(self) -> Optional[str]:
        response = await self.read_message(self.queue_name)
        return response['body'] if response else None

    async def resolve_topic(self) -> bool:
        if not await self.topic_exists(self.topic_name):
            await self.create_topic(self.topic_name)
            await self.create_queue(
                self.queue_name,
                self.topic_name,
                self.routing_key
            )
            return True

        logger.info(
            "Topic already exists",
            extra={
                "topic_name": self.topic_name
            },)
        return False
