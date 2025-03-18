import os
from unittest.mock import Mock
import pytest
from src.feature.backup_photos_from.domain.repositories.media_manager import MediaManagerRepository
from src.feature.backup_photos_from.domain.entities.file import FileDescription
from src.feature.backup_photos_from.infrastructure.layers.file_manager.abstract import AbstractFileManagerLayer


@pytest.fixture
def file_manager_mock():
    return Mock()


@pytest.fixture
def repository(file_manager_mock: AbstractFileManagerLayer):
    return MediaManagerRepository(file_manager_mock)


def test_filter_midias(repository: MediaManagerRepository):
    # Test valid media files
    assert repository.filter_midias("image.jpg") is True
    assert repository.filter_midias("photo.jpeg") is True
    assert repository.filter_midias("picture.png") is True
    assert repository.filter_midias("animation.gif") is True
    assert repository.filter_midias("video.mp4") is True
    assert repository.filter_midias("video.mov") is True

    # Test invalid media files
    assert repository.filter_midias("document.pdf") is False
    assert repository.filter_midias("text.txt") is False


def test_list_all_midias_from_folder(repository: MediaManagerRepository,
                                     file_manager_mock: AbstractFileManagerLayer):
    # Arrange
    path = "/test/path"
    file_path_list = ["file2.png", "file3.txt",
                      "file1.jpg", "file4.jpeg", "file5.pdf"]
    file_manager_mock.list_files.return_value = file_path_list

    # Create mock file descriptions with different dates
    file_list = [
        FileDescription(
            name="file2.png",
            path="/test/path/file2.png",
            extension=".png",
            size=200,
            creation_date="2023-01-02T00:00:00",
            modification_date="2023-01-02T00:00:00",
            attributes={"is_directory": False, "exists": True}
        ),
        FileDescription(
            name="file1.jpg",
            path="/test/path/file1.jpg",
            extension=".jpg",
            size=100,
            creation_date="2023-01-01T00:00:00",
            modification_date="2023-01-01T00:00:00",
            attributes={"is_directory": False, "exists": True}
        ),
        FileDescription(
            name="file4.jpeg",
            path="/test/path/file4.jpeg",
            extension=".jpeg",
            size=400,
            creation_date="2023-01-04T00:00:00",
            modification_date="2023-01-04T00:00:00",
            attributes={"is_directory": False, "exists": True}
        )
    ]

    file_list_sorted = sorted(file_list, key=lambda file: file.creation_date)

    # Mock the from_file static method
    FileDescription.from_file = Mock(side_effect=file_list)

    # Act
    result = repository.list_all_midias_from_folder(path)

    # Assert
    file_manager_mock.list_files.assert_called_once_with(path)
    assert len(result) == 3
    # Check if the result is sorted by creation date
    assert result == file_list_sorted


def test_move_file(repository: MediaManagerRepository,
                   file_manager_mock: AbstractFileManagerLayer):
    # Arrange
    file = FileDescription(
        name="file1.jpg",
        path="/test/path/file1.jpg",
        extension=".jpg",
        size=100,
        creation_date="2023-01-01T00:00:00",
        modification_date="2023-01-01T00:00:00",
        attributes={"is_directory": False, "exists": True}
    )
    destination = "/dest/path"

    # Act
    repository.move_file(file, destination)

    # Assert
    file_manager_mock.move_file.assert_called_once_with(
        "/test/path/file1.jpg", destination)


def test_create_folder_with_existing_folder(repository: MediaManagerRepository,
                                            file_manager_mock: AbstractFileManagerLayer):
    # Arrange
    path = "/src/2023/01/01/image.jpg"
    creation_date = "2023-01-01T00:00:00"

    file_manager_mock.folder_exists.return_value = True

    # Act
    result = repository.create_date_folder(path, creation_date)

    # Assert
    file_manager_mock.create_folder.assert_not_called()
    assert result == path


def test_create_folder_with_non_existing_folder(repository: MediaManagerRepository,
                                                file_manager_mock: AbstractFileManagerLayer):
    # Arrange
    path = "/src/2023/01/01/image.jpg"
    creation_date = "2023-01-01T00:00:00"
    file_manager_mock.folder_exists.return_value = False
    file_manager_mock.create_folder.return_value = "/src/2023/01/01/image.jpg"

    # Act
    result = repository.create_date_folder(path, creation_date)

    # Assert
    file_manager_mock.create_folder.assert_called_once_with(
        "/src/2023/01/01/image.jpg")
    assert result == path

def test_create_folder_with_date_pattern(repository: MediaManagerRepository,
                                         file_manager_mock: AbstractFileManagerLayer):
    # Arrange
    path = "/src"
    creation_date = "2023-01-01T00:00:00"
    file_manager_mock.folder_exists.return_value = False
    file_manager_mock.create_folder.return_value = "/src/2023/01/01/image.jpg"

    # Act
    result = repository.create_date_folder(path, creation_date)

    # Assert
    file_manager_mock.create_folder.assert_called_once_with(
        "/src/2023/01/01")
    assert result == "/src/2023/01/01"
