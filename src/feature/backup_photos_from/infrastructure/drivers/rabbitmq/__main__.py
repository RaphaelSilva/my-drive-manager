import asyncio
import subprocess
import os

from src.feature.backup_photos_from.infrastructure.drivers.rabbitmq.adapter import (
    RabbitMQTopicClient, RabbitMQTopicClientData)

__all__ = [
    "RabbitMQTopicClient"
]


async def main():
    config = RabbitMQTopicClientData(
        host="192.168.1.107",
        port=5672,
        username="user",
        password="password",
        ssl=False,
        queue_name="test_sanity_queue",
        topic_name="test_sanity_topic",
        routing_key="test_sanity_routing_key"
    )
    client = RabbitMQTopicClient(config)

    if client and await client.connection_alive():
        print("RabbitMQ Topic Client initialized successfully.")
        if await client.resolve_topic():
            print(f"Topic '{client.topic_name}' created successfully.")
        for i in range(5):
            message = f"Message {i + 1}"
            await client.send_message(message)
            print(f"Sent message: {message}")

        await asyncio.sleep(0.5)

        while True:
            message = await client.receive_message()
            if message:
                print(f"Received message: {message}")
            else:
                print("No messages in the queue.")
                break

        try:
            project_root = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                          capture_output=True, text=True, check=True).stdout.strip()
            makefile_path = os.path.join(project_root, "Makefile")
            make_script_result = subprocess.run(["make", "-f", makefile_path,
                                                 f"QUEUE_NAME={config.queue_name}",
                                                 f"EXCHANGE_NAME={config.topic_name}",
                                                 "clean-queue", "clean-exchange"],
                                                check=True,
                                                capture_output=True,
                                                text=True)
            print("Script init.sh executed successfully.")
            print(make_script_result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error executing script init.sh: {e}")
            print(f"Return code: {e.returncode}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
        except FileNotFoundError:
            print(
                "Error: init.sh not found. Ensure the script is in the correct directory and is executable.")


if __name__ == "__main__":
    asyncio.run(main())
