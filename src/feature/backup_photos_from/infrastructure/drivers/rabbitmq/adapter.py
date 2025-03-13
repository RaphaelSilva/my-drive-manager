import os
import aio_pika

from src.feature.backup_photos_from.infrastructure.factories.queue.abstract import AbstractQueueLayer


class RabbitMQClient(AbstractQueueLayer):
    def __init__(self,
                 queue_name: str,
                 host: str = os.getenv("RABBITMQ_HOST"),
                 port: int = int(os.getenv("RABBITMQ_PORT")),
                 user: str = os.getenv("RABBITMQ_USER"),
                 password: str = os.getenv("RABBITMQ_PASSWORD")):
        super().__init__(queue_name)
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None
        self.channel = None
        self.queue = None

    async def connect(self):
        self.connection = await aio_pika.connect(
            host=self.host,
            port=self.port,
            login=self.user,
            password=self.password,
        )
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def send_message(self, message: str):
        if self.channel is None or self.queue is None:
            raise Exception("Not connected to RabbitMQ")
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=self.queue_name,
        )

    async def receive_messages(self, max_messages: int) -> list[str]:
        if self.channel is None or self.queue is None:
            raise Exception("Not connected to RabbitMQ")
        messages = []
        async for message in self.queue:
            async with message.process():
                messages.append(message.body.decode())
                if len(messages) >= max_messages:
                    break
        return messages
    
    async def delete_message(self, receipt_handle: str):
        if self.channel is None or self.queue is None:
            raise Exception("Not connected to RabbitMQ")
        await self.channel.basic_client_ack(receipt_handle)