import asyncio
from src.feature.backup_photos_from.infrastructure.drivers.rabbitmq.adapter import RabbitMQTopicClient, RabbitMQTopicClientData

__all__ = [
    "RabbitMQTopicClient"
]


async def main():
    client = RabbitMQTopicClient(
        RabbitMQTopicClientData(
            host="192.168.1.107",
            port=5672,
            username="user",
            password="password",
            ssl=False,
            queue_name="test_sanity_queue",
            topic_name="test_sanity_topic",
            routing_key="test_sanity_routing_key"
        )
    )

    if client and await client.connection_alive():
        print("RabbitMQ Topic Client initialized successfully.")
        if await client.resolve_topic():
            print(f"Topic '{client.topic_name}' created successfully.")
        # for i in range(500):
        #     message = f"Message {i + 1}"
        #     await client.send_message(message)
        #     print(f"Sent message: {message}")
        # await asyncio.sleep(0.5)

        message = await client.receive_message()
        if message:
            print(f"Received message: {message}")
        else:
            print("No messages in the queue.")


if __name__ == "__main__":    
    asyncio.run(main())
