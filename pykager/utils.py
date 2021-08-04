import ast
import functools
import json
import platform
import sys
from typing import Any

is_windows = platform.system() == "Windows"


def cached_property(func):
    """
    returns different cache decorator based on python version.
    :type func: function
    """
    if sys.version_info > (3, 8):
        return functools.cached_property(func)
    return property(functools.lru_cache()(func))


def safe_eval(data: str) -> Any:
    """
    safest type i can manage eval w/o deps.
    by no means perfect,
    but data from user's own projects should be safe.
    """
    # string-list to list
    if ", " in data:
        return data.split(", ")
    # string-boolean to boolean
    elif data.lower() in {"true", "false"}:
        return data.lower() == "true"
    # json to dict/list
    try:
        # print(json.loads(data))
        return json.loads(data)
    except json.JSONDecodeError:
        pass
    # literal eval w/ ast
    try:
        return ast.literal_eval(data)
    except (ValueError, SyntaxError, TypeError):
        pass
    return data
