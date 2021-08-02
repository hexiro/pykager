from typing import List, Union


class Import:

    def __init__(self, *, import_: Union[str, List[str]], from_: str = None):
        self.from_ = from_
        self.import_ = import_
        if self.from_:
            if isinstance(import_, str):
                self.import_ = [import_]
        elif isinstance(self.import_, list):
            self.import_ = import_[0]

    @property
    def code(self):
        if self.from_:
            return f"from {self.from_} import {', '.join(self.import_)}"
        return f"import {self.import_}"
