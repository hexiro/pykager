from pathlib import Path
from typing import Optional

from pykager.utils import cached_property


class Readme:
    readme_extensions = {
        # as according to https://github.com/github/markup/tree/master#markups
        # and https://packaging.python.org/guides/making-a-pypi-friendly-readme/#creating-a-readme-file
        # Markdown
        ".markdown": "text/markdown",
        ".mdown": "text/markdown",
        ".mkdn": "text/markdown",
        ".md": "text/markdown",
        # Plain Text
        ".txt": "text/plain",
        "": "text/plain",
        # reStructuredText
        ".rst": "text/x-rst"
    }

    def __init__(self, directory: Path):
        self.__directory = directory

    @cached_property
    def readme(self) -> Optional[Path]:
        """
        Finds readme files in the specified directory
        README is case insensitive afaik
        """
        for f in self.directory.glob("*"):
            if f.name.upper().startswith("README") and f.suffix in self.readme_extensions:
                return f

    @cached_property
    def content_type(self) -> Optional[str]:
        if self.readme:
            return self.readme_extensions[self.readme.suffix]

    @property
    def directory(self):
        return self.__directory


if __name__ == "__main__":
    r = Readme(Path.cwd().parents[1])
    print(r.readme)
