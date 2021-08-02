from abc import ABC, abstractmethod


class Snippet(ABC):
    """
    Generate code for kwarg in setup.py
    """

    def __init__(self, variable: str):
        self.__variable = variable

    @property
    @abstractmethod
    def code(self) -> str:
        pass

    @property
    def variable(self) -> str:
        return self.__variable


class DetailedSnippet(Snippet):
    """
    Generate code for kwarg in setup.py
    Has context of other kwargs
    """

    def __init__(self, pykager, variable: str):
        """
        :type pykager: Pykager
        """
        super().__init__(variable)
        self.__pykager = pykager

    @property
    @abstractmethod
    def code(self) -> str:
        pass

    @property
    def pykager(self):
        return self.__pykager
