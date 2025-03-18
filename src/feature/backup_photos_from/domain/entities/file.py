import base64
import json
import os
import datetime


class FileDescription:
    def __init__(self, name: str, path: str, extension: str, size: int, creation_date: str, modification_date: str, attributes: dict):
        self.name = name
        self.path = path
        self.extension = extension
        self.size = size
        self.creation_date = creation_date
        self.modification_date = modification_date
        self.attributes = attributes

    @staticmethod
    def from_file(file_path: str) -> 'FileDescription':
        """
        Extract file information and create a FileDescription object.

        Args:
            file_path: Path to the file to process

        Returns:
            FileDescription object with extracted metadata
        """

        # Extract file information
        file_name = os.path.basename(file_path)
        extension = os.path.splitext(file_name)[1].lower()
        size = os.path.getsize(file_path)

        # Get timestamps and convert to string
        ctime = os.path.getctime(file_path)
        mtime = os.path.getmtime(file_path)
        creation_date = datetime.datetime.fromtimestamp(ctime).isoformat()
        modification_date = datetime.datetime.fromtimestamp(mtime).isoformat()

        # Additional attributes
        attributes = {
            "is_directory": os.path.isdir(file_path),
            "exists": os.path.exists(file_path),
        }

        return FileDescription(
            name=file_name,
            path=file_path,
            extension=extension,
            size=size,
            creation_date=creation_date,
            modification_date=modification_date,
            attributes=attributes
        )

    def to_base64(self) -> str:
        with open(self.path, "rb") as file:
            encoded_string = base64.b64encode(file.read())
            return encoded_string.decode("ascii")

    def to_json(self) -> dict:
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_string: str):
        data = json.loads(json_string)
        return cls(**data)

    def __str__(self):
        return f"FileDescription(file_name={self.name}, file_path={self.path})"

    def __repr__(self):
        return str(self)
