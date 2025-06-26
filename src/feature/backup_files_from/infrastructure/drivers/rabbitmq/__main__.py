import asyncio
import subprocess
import os
import argparse

from src.feature.backup_files_from.infrastructure.drivers.rabbitmq.adapter import (
    RabbitMQTopicClient, RabbitMQTopicClientData)

DIV = "-" * 88


def new_queue():
    data = RabbitMQTopicClientData()
    client = RabbitMQTopicClient(data)
    print(f"""{DIV}
Creating new queue with name: {client.queue_name},
topic name: {client.topic_name},
routing key: {client.routing_key}
host: {client.host},
port: {client.port},
username: {client.username},
password: {client.password},
{DIV}""")
    topic_was_created = asyncio.run(client.resolve_topic())
    print(f"Queue {"CREATED" if topic_was_created else "NOT CREATED"}!")


async def sanity_check():
    config = RabbitMQTopicClientData(
        queue_name="test_sanity.queue",
        topic_name="test_sanity.topic",
        routing_key="test_sanity.routing_key"
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
            project_root = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, check=True).stdout.strip()
            makefile_path = os.path.join(project_root, "Makefile")
            make_script_result = subprocess.run([
                "make", "-f", makefile_path,
                f"QUEUE_NAME={config.queue_name}",
                f"EXCHANGE_NAME={config.topic_name}",
                "clean-queue", "clean-exchange"
            ],
                check=True,
                capture_output=True,
                text=True
            )
            print("Script init.sh executed successfully.")
            print(make_script_result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error executing script make clean-*: {e}")
            print(f"Return code: {e.returncode}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
        except FileNotFoundError:
            print(
                "Error: command not found. Ensure the script is in the correct directory and is executable.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a specific function.")
    parser.add_argument("-r", "--run", type=str,
                        help="Name of the function to run (new_queue, main).", default="main")

    args = parser.parse_args()

    all_functions = {
        "new_queue": new_queue,
        "sanity_check": sanity_check,
    }

    if args.run not in all_functions:
        print(f"Available functions: {', '.join(all_functions.keys())}")
        exit(1)

    if args.run == "sanity_check":
        asyncio.run(all_functions[args.run]())
    else:
        all_functions[args.run]()
