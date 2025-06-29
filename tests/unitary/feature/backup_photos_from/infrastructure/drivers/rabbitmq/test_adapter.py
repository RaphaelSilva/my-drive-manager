import os
import re
from unittest.mock import AsyncMock, patch

import pytest

from src.feature.backup_files_from.infrastructure.drivers.rabbitmq.adapter import \
    RabbitMQTopicClient


@pytest.mark.asyncio
@patch.object(RabbitMQTopicClient, "create_message", new_callable=AsyncMock)
async def test_send_message(mock_create_message):
    os.environ["RABBITMQ_TOPIC_NAME"] = "test_topic"
    os.environ["RABBITMQ_ROUTING_KEY"] = "test_routing_key"
    client = RabbitMQTopicClient()
    message = "test message"
    await client.send_message(message)
    mock_create_message.assert_awaited_once_with(
        client.topic_name, client.routing_key, message)


@pytest.mark.asyncio
@patch.object(RabbitMQTopicClient, "create_message", new_callable=AsyncMock)
async def test_send_message_dlq(mock_create_message):
    os.environ["RABBITMQ_TOPIC_NAME"] = "test_topic"
    os.environ["RABBITMQ_ROUTING_KEY"] = "test_routing_key"
    client = RabbitMQTopicClient()
    message = "test message"
    await client.send_message_dlq(message)
    mock_create_message.assert_awaited_once_with(
        f'{client.topic_name}.dlq', client.routing_key, message)


@pytest.mark.asyncio
@patch.object(RabbitMQTopicClient, "read_message", new_callable=AsyncMock)
async def test_receive_message(mock_read_message):
    os.environ["RABBITMQ_TOPIC_NAME"] = "test_topic"
    os.environ["RABBITMQ_ROUTING_KEY"] = "test_routing_key"
    client = RabbitMQTopicClient()
    mock_read_message.return_value = {'body': 'test message'}
    response = await client.receive_message()
    mock_read_message.assert_awaited_once_with(client.topic_name)
    assert response == 'test message'


@pytest.mark.asyncio
@patch.object(RabbitMQTopicClient, "get_client", new_callable=AsyncMock)
async def test_create_message(mock_get_client):
    topic_name = "test_topic"
    routing_key = "test_routing_key"
    os.environ["RABBITMQ_TOPIC_NAME"] = topic_name
    os.environ["RABBITMQ_ROUTING_KEY"] = routing_key
    mock_topic = AsyncMock()
    mock_topic.publish = AsyncMock()
    mock_topic.publish.return_value = None
    mock_channel = AsyncMock()
    mock_channel.declare_exchange = AsyncMock()
    mock_channel.declare_exchange.return_value = mock_topic
    mock_channel.publisher_confirms = True
    mock_client = AsyncMock()
    mock_client.is_closed = False
    mock_client.channel = AsyncMock()
    mock_client.channel.return_value = mock_channel
    mock_get_client.return_value = mock_client


    client = RabbitMQTopicClient()    
    message = "test message"
    response = await client.create_message(topic_name, routing_key, message)
    assert response.get("confirmation")
    assert isinstance(response.get("message_id"), str)
    assert re.match(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        response.get("message_id"),
    ), "Message ID is not a valid UUID"
    mock_get_client.assert_called_once()
    mock_client.channel.assert_called_once()
    mock_channel.declare_exchange.assert_awaited_once_with(topic_name, 'topic')
    mock_topic.publish.assert_awaited_once()
    mock_client.close.assert_awaited_once()