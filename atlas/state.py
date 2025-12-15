# atlas/state.py

import time
from datetime import datetime, timezone
from typing import Optional


class AtlasState:
    """
    AtlasState is the in-memory runtime state of the ATLAS server.
    """

    def __init__(self) -> None:
        # Record when the server started (seconds)
        self._start_time: float = time.time()

        # Total number of HTTP requests handled
        self._requests_total: int = 0

        # timestamp of the last request (UTC)
        self._last_request_time: Optional[str] = None

    def mark_request(self) -> None:
        """
        Called on every HTTP request.

        Updates:
        - request counter
        - last request timestamp
        """
        self._requests_total += 1
        self._last_request_time = datetime.now(timezone.utc).isoformat()

    # State accessors

    def uptime_seconds(self) -> float:
        """
        Returns how long the server has been running.
        """
        return time.time() - self._start_time

    def requests_total(self) -> int:
        """
        Returns total number of requests handled.
        """
        return self._requests_total

    def last_request_time(self) -> Optional[str]:
        """
        Returns the last request timestamp, or None if no requests yet.
        """
        return self._last_request_time
