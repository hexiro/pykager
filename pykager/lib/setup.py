from pathlib import Path


class Setup:

    def __init__(self, directory: Path):
        self.__file = directory / "setup.py"
