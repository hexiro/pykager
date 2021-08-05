from pathlib import Path
from typing import Optional

from ..utils import safe_eval


class Init:

    def __init__(self, pykager):
        self.__pykager = pykager
        self.__name = self.pykager.name
        self.__kwargs = self.find_kwargs()

    def __getattr__(self, item):
        return self.kwargs.get(item)

    @property
    def pykager(self):
        return self.__pykager

    @property
    def kwargs(self):
        if self.__name != self.pykager.name:
            self.__kwargs = self.find_kwargs()
        return self.__kwargs

    @property
    def init_file(self) -> Optional[Path]:
        if self.__name:
            return self.pykager.input_dir / self.__name / "__init__.py"

    def find_kwargs(self) -> dict:
        if not self.init_file or not self.init_file.is_file():
            return {}
        code = self.init_file.read_text(encoding="utf-8", errors="ignore")
        kwargs = {}
        for line in code.splitlines():
            if not line.startswith("__") and "=" in line:
                continue
            key, value = line.split("=", maxsplit=1)
            key = key.strip().strip('_')
            value = safe_eval(value.strip())
            kwargs[key] = value
        return kwargs
