import platform
import subprocess

from pathlib import Path
from typing import List

is_windows = platform.system() == "Windows"
readme_extensions = {
    # as according to https://github.com/github/markup/tree/master#markups
    ".markdown", ".mdown", ".mkdn", ".md",  # Markdown
    ".textile",  # Textile
    ".rdoc",  # RDoc
    ".org",
    ".creole",
    ".mediawiki", ".wiki",
    ".rst",  # reStructuredText
    ".asciidoc", ".adoc", ".asc",  # AsciiDoc
    ".pod"
}


def clear():
    """
    Clears the console.
    uses "cls" for windows
    uses "clear" for unix
    """
    subprocess.Popen("cls" if is_windows else "clear", shell=True).wait()


def find_readme_files(directory: Path) -> List[Path]:
    """
    Finds readme files in the specified directory
    README is case insensitive afaik
    """
    return [f for f in directory.glob("README.*") if f.suffix in readme_extensions]
