

from abc import ABC, abstractmethod
from datetime import datetime

class MediaInfoError(Exception): ...

class AbstractMediaInfoLayer(ABC):

    @abstractmethod
    def extractDate(self) -> datetime:
        raise NotImplementedError

    @abstractmethod
    def resumeInfo(self) -> dict:
        raise NotImplementedError
