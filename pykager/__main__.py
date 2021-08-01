from argparse import ArgumentParser
from pathlib import Path

from pykager.lib import Git, Setup
from pykager.utils import cached_property


class Pykager(ArgumentParser):

    def __init__(self):
        super().__init__()
        self.add_argument("-i", "--input", help="input directory (default: cwd)")

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
    print(p.git.author)
