import base64
import json
import os
import tempfile
from datetime import datetime, timedelta

import pytest

from src.feature.backup_photos_from.domain.entities.file import FileDescription


@pytest.fixture(autouse=True)
def get_temp_file():
    temp_path = None

    def generate_temp_file():
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(b'Test content')
            temp_path = temp_file.name
        return temp_path
    try:
        yield generate_temp_file
    finally:
        # Clean up by removing the temporary file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def test_create_file_description():
    file_description = FileDescription(
        name="test.jpg",
        path="/path/to/file",
        extension="jpg",  # removed leading dot
        size=1024,
        creation_date="2023-01-01",
        modification_date="2023-01-02",
        attributes={}
    )
    assert file_description.name == "test.jpg"
    assert file_description.path == "/path/to/file"
    assert file_description.extension == "jpg"  # adjusted assertion
    assert file_description.size == 1024
    assert file_description.creation_date == "2023-01-01"
    assert file_description.modification_date == "2023-01-02"
    assert file_description.attributes == {}


def test_create_file_description_from_file(get_temp_file):
    # Define a time range for the file creation
    start_time = datetime.now() - timedelta(minutes=1)

    # Get the temporary file path
    temp_path = get_temp_file()

    # Call the from_file method
    file_description = FileDescription.from_file(temp_path)

    # Assert the file description has expected attributes
    assert file_description.name == os.path.basename(temp_path)
    assert file_description.path == temp_path
    assert file_description.extension == '.jpg'
    assert file_description.size > 1
    assert isinstance(file_description.creation_date, str)
    assert isinstance(file_description.modification_date, str)
    assert isinstance(file_description.attributes, dict)
    # Import datetime for timestamp verification
    end_time = datetime.now()

    # Parse the creation date string into a datetime object
    try:
        creation_time = datetime.fromisoformat(
            file_description.creation_date)
        # Assert the file was created within the expected time range
        assert start_time <= creation_time <= end_time, \
            f"File creation time {creation_time} not between {start_time} and {end_time}"
    except ValueError:
        assert False, f"Could not parse creation_date format: {file_description.creation_date}"


def test_file_description_to_base64(get_temp_file):
    file_description = FileDescription(
        name="test.jpg",
        path="/path/to/file",
        extension="jpg",
        size=1024,
        creation_date="2023-01-01",
        modification_date="2023-01-02",
        attributes={}
    )

    temp_path = get_temp_file()

    with open(temp_path, "rb") as file:
        encoded_string = base64.b64encode(file.read())
        expected_string = encoded_string.decode("ascii")

    # Call the to_base64 method
    file_description.path = temp_path

    encoded_string = file_description.to_base64()
    # Assert the encoded string is not empty
    assert encoded_string == expected_string, \
        f"Encoded string {encoded_string} does not match expected {expected_string}"


def test_file_description_to_json():
    file_description = FileDescription(
        name="test.jpg",
        path="/path/to/file",
        extension="jpg",
        size=1024,
        creation_date="2023-01-01",
        modification_date="2023-01-02",
        attributes={}
    )

    # Call the to_json method
    json_string = file_description.to_json()

    # Assert the json string is not empty
    assert json_string, "JSON string is empty"
    # Assert the json string is valid
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError:
        assert False, "Invalid JSON string"

    # Assert the json data has expected keys
    assert 'name' in data
    assert 'path' in data
    assert 'extension' in data
    assert 'size' in data
    assert 'creation_date' in data
    assert 'modification_date' in data
    assert 'attributes' in data

    assert data['name'] == file_description.name
    assert data['path'] == file_description.path
    assert data['extension'] == file_description.extension
    assert data['size'] == file_description.size
    assert data['creation_date'] == file_description.creation_date
    assert data['modification_date'] == file_description.modification_date
    assert data['attributes'] == file_description.attributes

def test_file_description_from_json():
    file_description = FileDescription(
        name="test.jpg",
        path="/path/to/file",
        extension="jpg",
        size=1024,
        creation_date="2023-01-01",
        modification_date="2023-01-02",
        attributes={}
    )

    # Call the to_json method
    json_string = file_description.to_json()

    # Call the from_json method
    new_file_description = FileDescription.from_json(json_string)

    # Assert the new file description is not empty
    assert new_file_description, "New FileDescription object is empty"
    # Assert the new file description is equal to the original
    assert new_file_description.name == file_description.name
    assert new_file_description.path == file_description.path
    assert new_file_description.extension == file_description.extension
    assert new_file_description.size == file_description.size
    assert new_file_description.creation_date == file_description.creation_date
    assert new_file_description.modification_date == file_description.modification_date
    assert new_file_description.attributes == file_description.attributes

def test_file_description_from_json_invalid():
    # Call the from_json method with an invalid JSON string
    with pytest.raises(json.JSONDecodeError):
        FileDescription.from_json("invalid json string")

def test_file_description_from_json_missing_keys():
    # Create a JSON string with missing keys
    json_string = '{"name": "test.jpg", "path": "/path/to/file", "size": 1024}'
    # Call the from_json method
    with pytest.raises(TypeError):
        FileDescription.from_json(json_string)

def test_file_description_from_json_extra_keys():
    # Create a JSON string with extra
    json_string = '{"name": "test.jpg", "path": "/path/to/file", "size": 1024, "extra": "value"}'
    with pytest.raises(TypeError):
        FileDescription.from_json(json_string)
