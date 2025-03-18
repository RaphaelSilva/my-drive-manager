

from abc import ABC, abstractmethod


class AbstractFileManagerLayer(ABC):

    @abstractmethod
    def get_files_in_folder(self, path: str) -> list[str]:
        raise NotImplementedError
