from argparse import ArgumentParser
from pathlib import Path

from pykager.lib import Git, Setup
from pykager.snippets import Snippet, Requirements, Readme
from pykager.utils import cached_property


class Pykager(ArgumentParser):
    __slots__ = (
        "name",
        "version",
        "author",
        "author_email",
        "url",
        "license",
        "description",
        "long_description",
        "keywords",
        "classifiers",
        "install_requires",
        "python_requires",
        "zip_safe",
        "packages",
        "entry_points",
    )

    def __init__(self):
        super().__init__()
        self.add_argument("-i", "--input", help="input directory (default: cwd)")
        self.name = self.setup_py.name or self.git.name
        self.version = self.setup_py.version
        self.author = self.setup_py.author or self.git.author.name
        self.author_email = self.setup_py.author_email or self.git.author.email
        self.url = self.setup_py.url or self.git.url
        self.license = self.setup_py.license
        self.description = self.setup_py.description
        self.long_description = self.readme
        self.keywords = self.setup_py.keywords
        self.classifiers = self.setup_py.classifiers
        self.install_requires = self.requirements
        self.python_requires = self.setup_py.python_requires
        self.zip_safe = self.setup_py.zip_safe
        self.packages = self.setup_py.packages

    @cached_property
    def git(self):
        return Git(self.input_dir)

    @cached_property
    def setup_py(self):
        return Setup(self.input_dir)

    @cached_property
    def readme(self):
        return Readme(self.input_dir)

    @cached_property
    def requirements(self):
        return Requirements(self.input_dir)

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

    @property
    def setup_args(self) -> dict:
        return {arg: getattr(self, arg) for arg in self.__slots__}

    @property
    def code(self) -> str:
        code = "from setuptools import setup\n" \
               "\n"

        setup_args = self.setup_args

        for arg, value in setup_args.items():
            if isinstance(value, Snippet):
                code += value.code
                code += "\n"

        code += "setup(\n"

        for arg, value in setup_args.items():
            value_repr = value.variable if isinstance(value, Snippet) else repr(value)
            if value is not None:
                code += f"    {arg}={value_repr},\n"
        return code + ")\n"

    def write(self):
        (self.input_dir / "setup.py").write_text(self.code, encoding="utf8", errors="strict")

    def cli_prompt(self):
        print("Preparing to generate a setup.py file.\n"
              "Press enter to leave blank or use the default listed.\n"
              "Separate list items with a comma and a space.\n")
        for arg, default in self.setup_args.items():
            if isinstance(default, Snippet):
                continue
            if isinstance(default, list):
                default = ", ".join(default)
            default = f" ({default})" if default else ""
            value = input(f"{arg}{default}: ")
            if ", " in value:
                value = value.split(", ")
            elif value.lower() in {"true", "false"}:
                value = value.lower() == "true"
            if value:
                setattr(self, arg, value)

        confirmation = input(
            "\n"
            f"About to write to setup.py\n"
            "\n"
            f"{self.code}\n"
            "\n"
            "is this okay? (yes): "
        )
        if confirmation == "" or confirmation.lower().startswith("y"):
            self.write()


def main():
    p = Pykager()
    p.cli_prompt()


if __name__ == "__main__":
    main()
