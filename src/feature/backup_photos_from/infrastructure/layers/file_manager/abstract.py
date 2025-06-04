

from abc import ABC, abstractmethod


class AbstractFileManagerLayer(ABC):

    @abstractmethod
    def list_files(self, path: str) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def move_file(self, source: str, destination: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_folder(self, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_folder(self, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def rename_file(self, path: str, new_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def file_exists(self, path: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def folder_exists(self, path: str) -> bool:
        raise NotImplementedError

