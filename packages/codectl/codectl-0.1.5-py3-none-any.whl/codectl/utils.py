"""Utilities"""

from pathlib import Path
import sys
import inspect
import importlib
import json
from typing import Iterable, Callable, Tuple
from codectl import settings
from functools import reduce
from operator import getitem


def retrieve_nested_value(dict_: dict, key_path: str):
    """使用reduce和getitem从嵌套字典中取值"""
    return reduce(getitem, key_path.split("."), dict_)


def get_user_config() -> dict:
    """
    Retrieves application configuration as a dictionary.

    Loads the configuration from a predefined JSON file specified by `settings.CONFIG_PATH`.
    If the configuration file does not exist, it creates an empty JSON file at that location.

    Returns:
        dict: A dictionary containing the configuration settings. Returns an empty dictionary
              if the configuration file is newly created or contains no settings.

    Example:
        >>> config = get_user_config()
        >>> print(config)
        {'setting1': 'value1', 'setting2': 'value2'}
    """

    config = {}

    if settings.CONFIG_PATH.is_file():
        config.update(json.loads(settings.CONFIG_PATH.read_text()))
    else:
        settings.CONFIG_PATH.write_text("{}")

    return config


def load_priv_funcs_from_mod(module_path: Path) -> Iterable[Tuple[str, Callable]]:
    """
    Loads private functions from a module.

    Imports a module by file path and returns private functions (names start with "_").
    Modifies `sys.path` if necessary for import.

    Args:
        module_path (Path): Path to the Python module.

    Returns:
        Iterable of (str, Callable) tuples for each private function.

    Example:
        funcs = load_priv_funcs_from_mod(Path('/path/to/module.py'))
        for name, func in funcs:
            print(name, func)
    """

    if not module_path.parent in sys.path:
        sys.path.append(str(module_path.parent))

    module = importlib.import_module(module_path.stem)

    return inspect.getmembers(
        module, lambda mem: inspect.isfunction(mem) and mem.__name__.startswith("_")
    )
