from pykager.snippets.snippet import DetailedSnippet


class ReadmeContentType(DetailedSnippet):

    def __init__(self, pykager):
        super().__init__(pykager)

    @property
    def code(self):
        return self.pykager.long_description.content_type

    @property
    def write_code(self) -> bool:
        return self.pykager.long_description.write_code
