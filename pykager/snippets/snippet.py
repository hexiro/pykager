from abc import ABC, abstractmethod
from typing import Union, List


class Snippet(ABC):
    """
    Generate code for kwarg in setup.py
    """

    def __init__(self, variable: str = None, imports: Union[str, List[str]] = None):
        self.__variable = variable
        self.__imports = imports

    @property
    @abstractmethod
    def code(self) -> str:
        pass

    @property
    @abstractmethod
    def write_code(self) -> bool:
        pass

    @property
    def variable(self):
        return self.__variable

    @property
    def imports(self):
        return self.__imports


class DetailedSnippet(Snippet):
    """
    Generate code for kwarg in setup.py
    Has context of other kwargs
    """

    def __init__(self, pykager, variable: str = None, imports: Union[str, List[str]] = None):
        """
        :type pykager: Pykager
        """
        super().__init__(variable, imports)
        self.__pykager = pykager

    @property
    @abstractmethod
    def code(self) -> str:
        pass

    @property
    @abstractmethod
    def write_code(self) -> bool:
        pass

    @property
    def pykager(self):
        return self.__pykager
