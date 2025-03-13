
from abc import ABC, abstractmethod
from typing import TypeVar

O = TypeVar('O')


class Business(ABC):  # type: ignore

    @abstractmethod
    def execute(self) -> O:
        '''Execute the business logic'''
