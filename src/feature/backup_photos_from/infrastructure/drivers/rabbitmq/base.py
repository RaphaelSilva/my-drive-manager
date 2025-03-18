import os
import uuid
import aio_pika
from aio_pika import DeliveryMode, ExchangeType, Message, exceptions
from aiormq import AMQPConnectionError

from src.shared.infrastructure.logging.syslog import logger


class RabbitMQBaseClient():
    def __init__(self) -> None:
        self.host = os.getenv("RABBITMQ_HOST")
        self.port = os.getenv("RABBITMQ_PORT")
        self.port = int(self.port) if self.port else 0
        self.username = os.getenv("RABBITMQ_USERNAME")
        self.password = os.getenv("RABBITMQ_PASSWORD")
        self.ssl = str(os.getenv("RABBITMQ_SSL")).lower() in [
            "on", "yes", "true"]
        if not self.host:
            raise ValueError(
                "host is not defined in environment RABBITMQ_HOST.")
        if not self.port:
            raise ValueError(
                "port is not defined in environment RABBITMQ_PORT.")
        if not self.username:
            raise ValueError(
                "username is not defined in environment RABBITMQ_USERNAME.")
        if not self.password:
            raise ValueError(
                "password is not defined in environment RABBITMQ_PASSWORD.")

    async def get_client(self):
        try:
            client = await aio_pika.connect(
                host=self.host,
                port=self.port,
                login=self.username,
                password=self.password,
                ssl=self.ssl,
            )

            return client
        except AMQPConnectionError as error:
            logger.error(
                "The application failed to connect to RabbitMQ: %s", error,
                extra={
                    "host": self.host,
                    "port": self.port,
                    "username": self.username,
                },
            )
            raise error
        except Exception as error:
            logger.error(
                "Generic error: %s", error,
                extra={
                    "host": self.host,
                    "port": self.port,
                    "username": self.username,
                },
            )
            raise error

    async def connection_alive(self):
        client = await self.get_client()
        status = client.is_closed
        await client.close()
        return status

    async def topic_exists(self, topic_name: str) -> bool:
        try:
            client = await self.get_client()
            channel = await client.channel()

            exchange = await channel.declare_exchange(
                topic_name, ExchangeType.TOPIC, passive=True
            )
            return exchange is not None
        except exceptions.ChannelClosed as error:
            print(f"Channel closed error: {error}")
            return False
        except Exception as error:
            raise error

    async def create_topic(self, topic_name: str):
        try:
            client = await self.get_client()
            channel = await client.channel()

            topic = await channel.declare_exchange(
                topic_name,
                ExchangeType.TOPIC,
            )
            return topic
        except Exception as error:
            raise error

    async def create_queue(self, queue_name: str, topic_name: str, routing_key: str):
        try:
            client = await self.get_client()
            channel = await client.channel()

            queue = await channel.declare_queue(queue_name, durable=True)
            topic = await channel.declare_exchange(topic_name, ExchangeType.TOPIC)

            await queue.bind(topic, routing_key=routing_key)
            return queue

        except Exception as error:
            raise error

    async def create_message(
        self, topic_name: str, routing_key: str, message_body: str
    ):
        client = None
        try:
            client = await self.get_client()
            channel = await client.channel()

            topic = await channel.declare_exchange(topic_name, ExchangeType.TOPIC)
            message_id = str(uuid.uuid4())

            message = Message(
                body=message_body.encode(),
                message_id=message_id,
                delivery_mode=DeliveryMode.PERSISTENT,
            )

            await topic.publish(message, routing_key=routing_key, mandatory=True)

            confirmation = channel.publisher_confirms
            response = {"message_id": message_id, "confirmation": confirmation}
            return response
        except Exception as error:
            raise error
        finally:
            if client is not None and not client.is_closed:
                await client.close()

    async def read_message(self, queue_name: str):
        client = None
        try:
            client = await self.get_client()
            channel = await client.channel()

            queue = await channel.declare_queue(queue_name, durable=True)
            message = await queue.get(no_ack=False)

            if not message:
                return None

            body = message.body.decode()
            response = {"message_id": message.message_id, "body": body}

            await message.ack()

            return response
        except Exception as error:
            raise error
        finally:
            if client is not None and not client.is_closed:
                await client.close()
