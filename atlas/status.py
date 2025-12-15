# atlas/status.py

from datetime import datetime, timezone
from typing import Dict, Any

from .state import AtlasState


VERSION = "0.0.2"


def build_health(state: AtlasState) -> Dict[str, Any]:
    """
    Build the health/status response for ATLAS.
    """
    
    return {
        "status": "ok",
        "version": VERSION,
        "uptime_seconds": state.uptime_seconds(),
        "server_time": datetime.now(timezone.utc).isoformat(),
        "requests_total": state.requests_total(),
        "last_request_time": state.last_request_time(),
    }
