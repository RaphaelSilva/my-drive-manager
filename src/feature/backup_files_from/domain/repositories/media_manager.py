import os
import re
from src.feature.backup_files_from.domain.entities.file import FileDescription
from src.feature.backup_files_from.infrastructure.layers.file_manager.abstract import AbstractFileManagerLayer


class MediaManagerRepository:

    def __init__(self, file_manager_layer: AbstractFileManagerLayer):
        self.file_manager = file_manager_layer

    def filter_midias(self, file: str) -> bool:
        return file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.heic', '.avi', '.mkv', '.webm'))

    def list_all_midias_from_folder(self, path: str) -> list[FileDescription]:
        files = map(
            FileDescription.from_file,
            filter(self.filter_midias, self.file_manager.list_files(path))
        )
        return sorted(files, key=lambda file: file.creation_date)

    def move_file(self, file: FileDescription, destination: str) -> None:
        self.file_manager.move_file(file.path, destination)

    def create_date_folder(self, folder_path: str, creation_date: str) -> str:
        # Check if the file path already contains date pattern (YYYY-MM-DD)
        date_pattern = re.compile(r'\d{4}/\d{2}/\d{2}')
        if date_pattern.search(folder_path):
            path = folder_path
        else:
            path = os.path.join(
                folder_path, *creation_date.split('T')[0].split('-'))
        if self.file_manager.folder_exists(path):
            return path
        self.file_manager.create_folder(path)
        return path
