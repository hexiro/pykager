from pathlib import Path
from typing import Optional

from pykager.snippets.snippet import Snippet
from pykager.utils import cached_property


class Requirements(Snippet):

    def __init__(self, directory: Path):
        self.__directory = directory

    @property
    def directory(self):
        return self.__directory

    @cached_property
    def requirements_file(self) -> Optional[Path]:
        if (self.directory / "requirements.txt").is_file():
            return self.directory / "requirements.txt"

    @property
    def code(self):
        return f"with open('{self.requirements_file.relative_to(self.directory)}', 'r') as req_file:\n" \
               f"    requirements = [l for l in req_file.read().splitlines() if l and not l.startswith('#')]\n"

    @property
    def variable(self):
        return "requirements"
