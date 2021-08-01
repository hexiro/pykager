from pathlib import Path
from typing import Optional

from pykager.utils import cached_property


class Readme:
    readme_extensions = {
        # as according to https://github.com/github/markup/tree/master#markups
        # and https://packaging.python.org/guides/making-a-pypi-friendly-readme/#creating-a-readme-file
        ".markdown", ".mdown", ".mkdn", ".md",  # Markdown
        ".rst",  # reStructuredText
        ".txt",  # plain text
    }

    def __init__(self, directory: Path):
        self.__directory = directory

    @cached_property
    def readme(self) -> Optional[Path]:
        """
        Finds readme files in the specified directory
        README is case insensitive afaik
        """
        search = [f for f in self.directory.glob("README.*") if f.suffix in self.readme_extensions]
        return search[0] if search else None

    @property
    def directory(self):
        return self.__directory
