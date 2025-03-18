from unittest.mock import MagicMock, Mock

import pytest

from src.feature.backup_photos_from.domain.business.media_queue_preparer import \
    MediaQueuePreparer
from src.feature.backup_photos_from.domain.repositories.media_manager import \
    MediaManagerRepository
from src.feature.backup_photos_from.domain.repositories.queue import \
    QueueRepository


@pytest.fixture
def mock_midia_repository():
    mock = Mock(spec=MediaManagerRepository)
    return mock


@pytest.fixture
def mock_queue_repository():
    mock = Mock(spec=QueueRepository)
    return mock


@pytest.fixture
def save_file_information(mock_midia_repository, mock_queue_repository):
    return MediaQueuePreparer(
        folder_source="/source/path",
        folder_destination="/destination/path",
        midia_repository=mock_midia_repository,
        queue_repository=mock_queue_repository
    )


def test_execute_should_put_file_information_in_queue(save_file_information: MediaQueuePreparer,
                                                      mock_midia_repository: MediaManagerRepository,
                                                      mock_queue_repository: QueueRepository):
    # Arrange
    mock_file1 = MagicMock()
    mock_file1.to_json.return_value = {"name": "file1.jpg", "size": 1024}
    mock_file2 = MagicMock()
    mock_file2.to_json.return_value = {"name": "file2.jpg", "size": 2048}
    mock_midia_repository.list_all_midias_from_folder.return_value = [
        mock_file1, mock_file2]

    # Act
    save_file_information.execute()

    # Assert
    mock_midia_repository.list_all_midias_from_folder.assert_called_once_with(
        "/source/path")
    assert mock_queue_repository.put.call_count == 2
    mock_queue_repository.put.assert_any_call({
        'file': {"name": "file1.jpg", "size": 1024},
        'source': "/source/path",
        'destination': "/destination/path"
    })
    mock_queue_repository.put.assert_any_call({
        'file': {"name": "file2.jpg", "size": 2048},
        'source': "/source/path",
        'destination': "/destination/path"
    })


def test_execute_with_empty_file_list(save_file_information: MediaQueuePreparer,
                                      mock_midia_repository: MediaManagerRepository,
                                      mock_queue_repository: QueueRepository):
    # Arrange
    mock_midia_repository.list_all_midias_from_folder.return_value = []

    # Act
    save_file_information.execute()

    # Assert
    mock_midia_repository.list_all_midias_from_folder.assert_called_once_with(
        "/source/path")
    mock_queue_repository.put.assert_not_called()
