import argparse
from pathlib import Path

from pykager.lib.git_ import Git


class Pykager(argparse.ArgumentParser):

    def __init__(self):
        super().__init__()
        self.add_argument("-i", "--input", help="input directory (default: cwd)")
        args = self.parse_args()

        if args.input:
            input_dir = Path(args.input).resolve()
        elif __name__ == "__main__":
            input_dir = Path.cwd().parent
        else:
            input_dir = Path.cwd()

        if not input_dir.is_dir():
            input_dir = input_dir.parent

        self.__input_dir = input_dir
        self.git = Git(self.input_dir)
        # self.setup_py = SetupPy()

    @property
    def input_dir(self):
        return self.__input_dir

    @property
    def default_name(self):
        name = self.input_dir.name
        if any(self.input_dir.glob(name)):
            return name


if __name__ == "__main__":
    p = Pykager()
    print(p.git.author)
