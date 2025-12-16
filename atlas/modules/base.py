# atlas/modules/base.py

from typing import Protocol

from fastapi import APIRouter

from ..config import Settings
from ..state import AtlasState


class AtlasModule(Protocol):
    name: str

    def router(self, *, state: AtlasState, settings: Settings) -> APIRouter:
        ...
