from argparse import ArgumentParser
from pathlib import Path
from typing import List

from .lib import Git, Setup, Init, Imports
from .snippets import Snippet, Requirements, Readme, ReadmeContentType, Packages
from .utils import cached_property, safe_eval


class Pykager:

    def __init__(self):
        super().__init__()
        # dynamic private things
        arg_parser = ArgumentParser()
        arg_parser.add_argument("-i", "--input", help="input directory (default: cwd)")
        self.__args = arg_parser.parse_args()

        # setup.py things
        self._name = None
        self._version = None
        self._description = None
        self._author = None
        self._author_email = None
        self._url = None
        self._license = None
        self._long_description = None
        self._long_description_content_type = None
        self._keywords = None
        self._classifiers = None
        self._python_requires = None
        self._install_requires = None
        self._zip_safe = None
        self._packages = None
        self._entry_points = None

    @cached_property
    def input_dir(self):
        if self.__args.input:
            input_dir = Path(self.__args.input).resolve()
        elif __name__ == "__main__":
            input_dir = Path.cwd().parent
        else:
            input_dir = Path.cwd()

        if not input_dir.is_dir():
            input_dir = input_dir.parent
        return input_dir

    @cached_property
    def git(self):
        return Git(self.input_dir)

    @cached_property
    def setup_py(self):
        return Setup(self.input_dir)

    @cached_property
    def init_py(self):
        return Init(self)

    # setup.py

    @property
    def name(self):
        return self.setup_py.name or self.git.name

    @property
    def version(self):
        return self.init_py.version or self.setup_py.version

    @property
    def description(self):
        return self.setup_py.description

    @property
    def author(self):
        return self.setup_py.author or self.git.author_name or self.init_py.author

    @property
    def author_email(self):
        return self.setup_py.author_email or self.init_py.email or self.git.author_email

    @property
    def url(self):
        return self.setup_py.url or self.git.url

    @property
    def license(self):
        return self.setup_py.license or self.init_py.license

    @property
    def long_description(self):
        return Readme(self.input_dir)

    @property
    def long_description_content_type(self):
        return ReadmeContentType(self)

    @property
    def keywords(self):
        return self.setup_py.keywords

    @property
    def classifiers(self):
        return self.setup_py.classifiers

    @property
    def python_requires(self):
        return self.setup_py.python_requires

    @property
    def install_requires(self):
        return Requirements(self.input_dir)

    @property
    def zip_safe(self):
        return self.setup_py.zip_safe

    @property
    def packages(self):
        return Packages(self)

    @property
    def entry_points(self):
        return self.setup_py.entry_points

    @property
    def setup_args(self) -> List[str]:
        return ["name", "version", "description", "author", "author_email", "url", "license", "long_description",
                "long_description_content_type", "keywords", "classifiers", "python_requires", "install_requires",
                "zip_safe", "packages", "entry_points"]

    @cached_property
    def code(self) -> str:
        imports = Imports(["from setuptools import setup"])

        setup_dict = {k: self.argument(k) for k in self.setup_args}

        code = ""

        for arg, value in setup_dict.items():
            if isinstance(value, Snippet) and value.write_code:
                imports.add_imports(value.imports)
                if value.variable:
                    code += value.code + "\n"

        watermark = "# setup.py generated by https://github.com/hexiro/pykager"
        code = imports.code + "\n\n" + watermark + "\n\n" + code + "setup(\n"

        for arg, value in setup_dict.items():
            if value is not None:
                if isinstance(value, Snippet):
                    if not value.write_code:
                        continue
                    value_code = value.variable or repr(value.code)
                else:
                    value_code = repr(value)
                code += f"    {arg}={value_code},\n"

        return code + ")\n"

    def argument(self, name: str):
        return getattr(self, f"_{name}") or getattr(self, name)

    def write(self):
        (self.input_dir / "setup.py").write_text(self.code, encoding="utf8", errors="strict")

    def cli_prompt(self):
        try:
            print("Preparing to generate a setup.py file.\n"
                  "Press enter to leave blank or use the default listed.\n"
                  "Separate list items with a comma and a space.\n")
            for arg in self.setup_args:
                clean_arg = arg.replace("_", " ")
                default = self.argument(arg)
                if isinstance(default, Snippet):
                    continue
                if isinstance(default, list):
                    default = ", ".join(default)
                default = f" ({default})" if default else ""
                value = safe_eval(input(f"{clean_arg}{default}: "))
                if value:
                    setattr(self, "_" + arg, value)

            print()

            if self.code.endswith("setup(\n)\n"):
                print("Not enough information was given to write a setup.py file.\n"
                      "Aborting.")
                return

            confirmation = input(
                f"About to write to setup.py\n"
                "\n"
                f"{self.code}\n"
                "\n"
                "is this okay? (yes): "
            )
            if confirmation == "" or confirmation.lower().startswith("y"):
                self.write()
        except KeyboardInterrupt:
            pass


def main():
    p = Pykager()
    p.cli_prompt()


if __name__ == "__main__":
    print(Pykager().code)
