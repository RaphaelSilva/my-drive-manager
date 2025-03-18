from unittest.mock import Mock

import pytest

from src.feature.backup_photos_from.domain.repositories.queue import \
    QueueRepository
from src.feature.backup_photos_from.infrastructure.layers.queue.abstract import \
    AbstractQueueLayer


@pytest.fixture
def queue_layer_mock():
    """Fixture for mocking the underlying queue layer."""
    return Mock()


@pytest.fixture
def queue_repository(queue_layer_mock: AbstractQueueLayer):
    """Fixture for creating a QueueRepository with a mocked queue layer."""
    return QueueRepository(queue_layer_mock)


def test_put_adds_item_to_queue(queue_repository: QueueRepository, queue_layer_mock: AbstractQueueLayer):
    """Test that put method adds an item to the queue via the layer."""
    test_item = {"path": "/test/path.jpg", "name": "path.jpg"}

    queue_repository.put(test_item)

    queue_layer_mock.send_message.assert_called_once_with(test_item)


def test_get_retrieves_item_from_queue(queue_repository: QueueRepository, queue_layer_mock: AbstractQueueLayer):
    """Test that get method retrieves an item from the queue via the layer."""
    expected_item = {"path": "/test/path.jpg", "name": "path.jpg"}
    queue_layer_mock.receive_messages.return_value = expected_item

    result = queue_repository.get()

    assert result == expected_item
    queue_layer_mock.receive_messages.assert_called_once()


def test_empty_checks_if_queue_is_empty(queue_repository: QueueRepository, queue_layer_mock: AbstractQueueLayer):
    """Test that empty method checks if the queue is empty via the layer."""
    queue_layer_mock.is_empty.return_value = True

    result = queue_repository.empty()

    assert result is True
    queue_layer_mock.is_empty.assert_called_once()


def test_size_returns_queue_size(queue_repository: QueueRepository, queue_layer_mock: AbstractQueueLayer):
    """Test that size method returns the queue size via the layer."""
    queue_layer_mock.size.return_value = 5

    result = queue_repository.size()

    assert result == 5
    queue_layer_mock.size.assert_called_once()

def test_dlq_sends_message_to_dlq(queue_repository: QueueRepository, queue_layer_mock: AbstractQueueLayer):
    """Test that dlq method sends a message to the dead letter queue."""
    test_message = {"path": "/test/path.jpg", "name": "path.jpg"}
    test_error = Exception("Test error")

    expected_message = test_message.copy()
    expected_message["error"] = test_error.__dict__

    queue_repository.dlq(test_message, test_error)

    queue_layer_mock.send_message_dlq.assert_called_once_with(expected_message)
    assert expected_message["error"] == test_error.__dict__
