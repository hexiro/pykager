from pykager.lib import Import
from pykager.snippets import DetailedSnippet


class Packages(DetailedSnippet):

    def __init__(self, pykager):
        super().__init__(pykager, "packages", [Import(from_="setuptools", import_=["find_packages"])])

    @property
    def code(self):
        name = self.pykager.name
        return f"packages = ['{name}'] + [('{name}.' + x) for x in find_packages(where='{name}')]\n"

    @property
    def write_code(self) -> bool:
        return isinstance(self.pykager.name, str)
