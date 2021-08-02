from argparse import ArgumentParser
from pathlib import Path

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
        self.name = self.__setup_py.name or self.__git.name
        self.version = self.__setup_py.version
        self.description = self.__setup_py.description
        self.author = self.__setup_py.author or self.__git.author.name
        self.author_email = self.__setup_py.author_email or self.__git.author.email
        self.url = self.__setup_py.url or self.__git.url
        self.license = self.__setup_py.license
        self.long_description = Readme(self.__input_dir)
        self.long_description_content_type = self.long_description.content_type
        self.keywords = self.__setup_py.keywords
        self.classifiers = self.__setup_py.classifiers
        self.python_requires = self.__setup_py.python_requires
        self.install_requires = Requirements(self.__input_dir)
        self.zip_safe = self.__setup_py.zip_safe
        self.packages = Packages(self)

    @property
    def setup_args(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

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
    p = Pykager()
    print(p.code)
