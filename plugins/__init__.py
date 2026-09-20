from __future__ import annotations

import importlib
import pkgutil
from types import ModuleType


def discover() -> dict[str, ModuleType]:
    found: dict[str, ModuleType] = {}
    package = importlib.import_module("plugins")
    for info in pkgutil.iter_modules(package.__path__, "plugins."):
        mod = importlib.import_module(info.name)
        name = info.name.rsplit(".", 1)[-1]
        if name.startswith("_"):
            continue
        found[name] = mod
    return found
