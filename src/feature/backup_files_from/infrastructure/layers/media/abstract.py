

from abc import ABC, abstractmethod
from datetime import datetime

class MediaInfoError(Exception): ...

class AbstractMediaInfoLayer(ABC):

    @abstractmethod
    def extractDate(self, path: str) -> datetime:
        raise NotImplementedError
