# atlas/config.py

import os
from dataclasses import dataclass
from typing import List, Optional


def _getenv(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _split_csv(value: str) -> List[str]:
    if not value.strip():
        return []
    return [x.strip() for x in value.split(",") if x.strip()]


@dataclass(frozen=True)
class Settings:
    version: str
    api_key: Optional[str]
    enabled_modules: List[str]
    open_paths: List[str]

    @staticmethod
    def load() -> "Settings":
        version = _getenv("ATLAS_VERSION", "0.0.2")

        api_key_raw = _getenv("ATLAS_API_KEY", "")
        api_key = api_key_raw if api_key_raw else None

        enabled_modules = _split_csv(_getenv("ATLAS_MODULES", "core"))

        # Endpoints allowed without auth
        open_paths = [
            "/health",
            "/whoami",
            "/modules",
        ]

        return Settings(
            version=version,
            api_key=api_key,
            enabled_modules=enabled_modules,
            open_paths=open_paths,
        )
