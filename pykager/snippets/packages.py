from ..snippets import DetailedSnippet


class Packages(DetailedSnippet):

    def __init__(self, pykager):
        super().__init__(pykager, "packages", "from setuptools import find_packages")

    @property
    def code(self):
        name = self.pykager.name
        return f"packages = ['{name}'] + [('{name}.' + x) for x in find_packages(where='{name}')]\n"

    @property
    def write_code(self) -> bool:
        return isinstance(self.pykager.name, str)
