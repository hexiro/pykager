from argparse import ArgumentParser
from pathlib import Path

from pykager.lib import Git, Setup
from pykager.utils import cached_property


class Pykager(ArgumentParser):

    def __init__(self):
        super().__init__()
        self.add_argument("-i", "--input", help="input directory (default: cwd)")
        self.name = None
        self.version = None
        self.author = None
        self.author_email = None
        self.maintainer = None
        self.maintainer_email = None
        self.url = None
        self.license = None
        self.description = None
        self.long_description = None
        self.keywords = None
        self.platforms = None
        self.classifiers = None
        self.download_url = None
        self.install_requires = None
        self.python_requires = None
        self.zip_safe = None
        self.packages = None
        self.entry_points = None

    @cached_property
    def git(self):
        return Git(self.input_dir)

    @cached_property
    def setup_py(self):
        return Setup(self.input_dir)

    @cached_property
    def args(self):
        return self.parse_args()

    @cached_property
    def input_dir(self):
        if self.args.input:
            input_dir = Path(self.args.input).resolve()
        elif __name__ == "__main__":
            input_dir = Path.cwd().parent
        else:
            input_dir = Path.cwd()

        if not input_dir.is_dir():
            input_dir = input_dir.parent
        return input_dir


if __name__ == "__main__":
    p = Pykager()
