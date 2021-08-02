from argparse import ArgumentParser
from pathlib import Path
from pprint import pprint

from pykager.lib import Git, Setup, Import
from pykager.snippets import Snippet, Requirements, Readme
from pykager.snippets.packages import Packages


class Pykager:

    def __init__(self):
        super().__init__()
        # dynamic private things
        arg_parser = ArgumentParser()
        arg_parser.add_argument("-i", "--input", help="input directory (default: cwd)")
        self.__args = arg_parser.parse_args()

        if self.__args.input:
            input_dir = Path(self.__args.input).resolve()
        elif __name__ == "__main__":
            input_dir = Path.cwd().parent
        else:
            input_dir = Path.cwd()

        if not input_dir.is_dir():
            input_dir = input_dir.parent

        self.__input_dir = input_dir
        self.__git = Git(self.__input_dir)
        self.__setup_py = Setup(self.__input_dir)

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

    @property
    def name(self):
        return self.__setup_py.name or self.__git.name

    @property
    def version(self):
        return self.__setup_py.version

    @property
    def description(self):
        return self.__setup_py.description

    @property
    def author(self):
        return self.__setup_py.author or self.__git.author.name

    @property
    def author_email(self):
        return self.__setup_py.author_email or self.__git.author.email

    @property
    def url(self):
        return self.__setup_py.url or self.__git.url

    @property
    def license(self):
        return self.__setup_py.license

    @property
    def long_description(self):
        return Readme(self.__input_dir)

    @property
    def long_description_content_type(self):
        return self.long_description.content_type

    @property
    def keywords(self):
        return self.__setup_py.keywords

    @property
    def classifiers(self):
        return self.__setup_py.classifiers

    @property
    def python_requires(self):
        return self.__setup_py.python_requires

    @property
    def install_requires(self):
        return Requirements(self.__input_dir)

    @property
    def zip_safe(self):
        return self.__setup_py.zip_safe

    @property
    def packages(self):
        return Packages(self)

    @property
    def setup_args(self) -> dict:
        args = ["name", "version", "description", "author", "author_email", "url", "license", "long_description",
                "long_description_content_type", "keywords", "classifiers", "python_requires", "install_requires",
                "zip_safe", "packages",
                ]
        return {k: getattr(self, f"_{k}") or getattr(self, k) for k in args}

    @property
    def code(self) -> str:
        imports = [Import(from_="setuptools", import_="setup")]

        for arg, value in self.setup_args.items():
            if isinstance(value, Snippet):
                for i in value.imports:
                    imports.append(i)

        code = "\n".join(i.code for i in imports) + "\n\n"

        for arg, value in self.setup_args.items():
            if isinstance(value, Snippet):
                code += value.code + "\n"

        code += "setup(\n"

        for arg, value in self.setup_args.items():
            if value is not None:
                value = value.variable if isinstance(value, Snippet) else repr(value)
                code += f"    {arg}={value},\n"

        return code + ")\n"

    def write(self):
        (self.__input_dir / "setup.py").write_text(self.code, encoding="utf8", errors="strict")

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
                setattr(self, "_" + arg, value)

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
