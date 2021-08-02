from abc import ABC, abstractmethod


class Snippet(ABC):

    @property
    @abstractmethod
    def code(self) -> str:
        pass

    @property
    @abstractmethod
    def variable(self):
        pass
