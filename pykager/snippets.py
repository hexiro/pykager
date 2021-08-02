from abc import abstractmethod, ABC
from pathlib import Path
from typing import Union


class Snippet(ABC):

    @property
    @abstractmethod
    def code(self) -> str:
        pass

    @property
    @abstractmethod
    def variable(self):
        pass


class Requirements(Snippet):

    def __init__(self, requirements_file: Union[str, Path]):
        if isinstance(requirements_file, Path):
            self.requirements_file = str(requirements_file.resolve())
        else:
            self.requirements_file = requirements_file

    @property
    def code(self):
        return f"with open('{self.requirements_file}', 'r') as req_file:\n" \
               f"    requirements = [l for l in req_file.read().splitlines() if l and not l.startswith('#')]\n"

    @property
    def variable(self):
        return "requirements"
