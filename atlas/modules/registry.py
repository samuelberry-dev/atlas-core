# atlas/modules/registry.py

from typing import Dict, List

from .base import AtlasModule
from .core import CoreModule


def available_modules() -> Dict[str, AtlasModule]:
    return {
        "core": CoreModule(),
    }


def load_modules(enabled: List[str]) -> List[AtlasModule]:
    avail = available_modules()
    loaded: List[AtlasModule] = []

    for name in enabled:
        m = avail.get(name)
        if m:
            loaded.append(m)

    if not any(m.name == "core" for m in loaded):
        loaded.insert(0, avail["core"])

    return loaded
