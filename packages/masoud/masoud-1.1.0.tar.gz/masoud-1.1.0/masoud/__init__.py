import importlib.metadata as _metadata

from ._cli import cli
from ._service import Service
from ._inventory import Inventory, Host, Group, Toml, TomlContainer


__all__ = [
    "cli",
    "Service",
    "Toml",
    "TomlContainer",
    "Host",
    "Group",
    "Inventory",
]

__version__ = _metadata.version("masoud")
