import os
from subprocess import call
from src.feature.backup_files_from.infrastructure.layers.file_manager.abstract import AbstractFileManagerLayer


class BaseDriverManeger(AbstractFileManagerLayer):
    def __init__(self):
        pass

    def list_files(self, path: str):
        """
        List files in the given path.

        Args:
            path (str): Path to list files from

        Returns:
            list: List of file paths
        """
        return [os.path.join(path, file) for file in os.listdir(path)]

    def move_file(self, source: str, destination: str):  # type: ignore
        """
        Copy file from source to destination.

        Args:
            source (str): Source file path
            destination (str): Destination file path

        Returns:
            bool: True if copy was successful
        """
        response = call(f"cp -p {source} {destination}", shell=True)
        return response == 0

    def delete_file(self, path):
        """
        Delete a file.

        Args:
            path (str): Path to the file
        """
        os.remove(path)

    def rename_file(self, path, new_name):
        """
        Rename a file.

        Args:
            path (str): Path to the file
            new_name (str): New name for the file
        """
        os.rename(path, new_name)

    def create_folder(self, path):
        """
        Create a folder.

        Args:
            path (str): Path to the folder
        """
        os.makedirs(path)

    def delete_folder(self, path):
        """
        Delete a folder.

        Args:
            path (str): Path to the folder
        """
        os.rmdir(path)

    def file_exists(self, path):
        """
        Check if a file exists.

        Args:
            path (str): Path to the file

        Returns:
            bool: True if file exists
        """
        return os.path.exists(path)

    def folder_exists(self, path):
        """
        Check if a folder exists.

        Args:
            path (str): Path to the folder

        Returns:
            bool: True if folder exists
        """
        return os.path.exists(path)
