# atlas/status.py

from datetime import datetime, timezone
from typing import Any, Dict

from .state import AtlasState
from .config import Settings


def build_health(state: AtlasState, *, settings: Settings) -> Dict[str, Any]:
    return {
        "status": "ok",
        "version": settings.version,
        "uptime_seconds": state.uptime_seconds(),
        "server_time": datetime.now(timezone.utc).isoformat(),
        "requests_total": state.requests_total(),
        "last_request_time": state.last_request_time(),
    }
