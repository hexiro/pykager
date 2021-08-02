from pykager.snippets import DetailedSnippet


class Packages(DetailedSnippet):

    def __init__(self, pykager):
        super().__init__(pykager, "packages")

    @property
    def code(self):
        name = self.pykager.name
        return f"['{name}'] + [('{name}.' + x) for x in find_packages(where='{name}')]"
