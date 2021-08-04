from typing import List, Union


class Imports(list):

    def __init__(self, import_: Union[str, List[str]]):
        if isinstance(import_, str):
            import_ = [import_]
        super().__init__(import_)

    def add_imports(self, imports: Union[str, List[str]]):
        if not imports:
            return
        if isinstance(imports, str):
            self.append(imports)
            return
        for i in imports:
            self.append(i)

    def sort_imports(self):
        """
        properly sorts imports to PEP8 standard
        """
        self.sort()
        if len(self) > 1:
            for index, element in enumerate(self):
                if element.startswith("import"):
                    self[:] = self[index:] + [""] + self[:index]
                    break

    @property
    def code(self):
        self.sort_imports()
        return "\n".join(self)
