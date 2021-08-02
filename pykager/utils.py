import ast
import functools
import platform
import subprocess
import sys
from typing import Any

is_windows = platform.system() == "Windows"


def cached_property(func):
    """
    returns different cache decorator based on python version
    :type func: function
    """
    if sys.version_info > (3, 8):
        return functools.cached_property(func)
    return property(functools.lru_cache()(func))


def clear():
    """
    Clears the console.
    uses "cls" for windows
    uses "clear" for unix
    """
    subprocess.Popen("cls" if is_windows else "clear", shell=True).wait()


def safe_eval(data: str) -> Any:
    try:
        return ast.literal_eval(data)
    except (ValueError, SyntaxError, TypeError):
        return
