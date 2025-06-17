import os
import uuid
from typing import Optional, TypedDict

import aio_pika
from aio_pika import DeliveryMode, ExchangeType, Message, exceptions
from aiormq import AMQPConnectionError
from pydantic import BaseModel

from src.shared.infrastructure.logging.syslog import logger


class RabbitMQBaseClientData(BaseModel):
    host: str
    port: int
    username: str
    password: str
    ssl: bool


class ReadMessageResponse(TypedDict):
    message: object
    body: str


class RabbitMQBaseClient():

    def __init__(self, data: Optional[RabbitMQBaseClientData] = None) -> None:
        super().__init__()
        self.host = data.host if data and data.host else os.getenv(
            "RABBITMQ_HOST", "localhost")
        port = data.port if data and data.port else os.getenv(
            "RABBITMQ_PORT",  "5672")
        self.port = int(port) if port else 0
        self.username = data.username if data and data.username else os.getenv(
            "RABBITMQ_USERNAME", "admin")
        self.password = data.password if data and data.password else os.getenv(
            "RABBITMQ_PASSWORD",  "xpto123")
        self.ssl = data.ssl if data and data.ssl else str(
            os.getenv("RABBITMQ_SSL", "no")).lower() == "true"

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
        status = not client.is_closed
        await client.close()
        return status

    async def topic_exists(self, topic_name: str) -> bool:
        client = None
        try:
            client = await self.get_client()
            channel = await client.channel()
            await channel.declare_queue()

            exchange = await channel.declare_exchange(
                topic_name, ExchangeType.TOPIC, passive=True
            )
            return exchange is not None
        except exceptions.ChannelClosed as error:
            logger.warning(f"Channel closed error at {topic_name}: %s", error)
            return False
        except Exception as error:
            logger.error("Generic error: %s", error)
            raise error
        finally:
            if client is not None and not client.is_closed:
                await client.close()

    async def create_topic(self, topic_name: str):
        client = None
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
        finally:
            if client is not None and not client.is_closed:
                await client.close()

    async def create_queue(self, queue_name: str, topic_name: str, routing_key: str):
        client = None
        try:
            client = await self.get_client()
            channel = await client.channel()

            queue = await channel.declare_queue(queue_name, durable=True)
            topic = await channel.declare_exchange(topic_name, ExchangeType.TOPIC)

            bindOk = await queue.bind(topic, routing_key=routing_key)
            logger.info(
                "Queue bound to topic successfully",
                extra={
                    "queue_name": queue_name,
                    "topic_name": topic_name,
                    "routing_key": routing_key,
                    "bind_ok": bindOk,
                }
            )
            return queue

        except Exception as error:
            raise error
        finally:
            if client is not None and not client.is_closed:
                await client.close()

    async def create_message(
        self, topic_name: str, routing_key: str, message_body: str
    ):
        client = None
        try:
            client = await self.get_client()
            channel = await client.channel()

            exchange = await channel.declare_exchange(topic_name, ExchangeType.TOPIC, durable=False)
            message_id = str(uuid.uuid4())

            message = Message(
                app_id='backup_photos_from',
                body=message_body.encode(),
                message_id=message_id,
                delivery_mode=DeliveryMode.PERSISTENT,
                content_type='application/json',
                content_encoding='utf-8',
            )

            ret = await exchange.publish(message, routing_key=routing_key, mandatory=True)

            confirmation = channel.publisher_confirms
            response = {
                "message_id": message_id,
                "confirmation": confirmation,
                "ret": ret
            }
            return response
        except Exception as error:
            raise error
        finally:
            if client is not None and not client.is_closed:
                await client.close()

    async def read_message(self, queue_name: str) -> Optional[ReadMessageResponse]:
        client = None
        try:
            client = await self.get_client()
            channel = await client.channel()

            queue = await channel.declare_queue(queue_name, durable=True)
            message = await queue.get()

            if not message or not message.message_id:
                return None

            body = message.body.decode()
            response: ReadMessageResponse = {
                "body": body,
                "message": message or None}

            await message.ack()  # Acknowledge the message

            return response

        except exceptions.QueueEmpty:
            return None
        except Exception as error:
            logger.error("Error reading message: %s", error)
            raise error
        finally:
            if client is not None and not client.is_closed:
                await client.close()
