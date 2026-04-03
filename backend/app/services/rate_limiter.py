"""In-memory IP-based rate limiter for the demo chat endpoint."""

import threading
from collections import defaultdict
from datetime import UTC, datetime, timedelta


class RateLimiter:
    def __init__(self, limit: int, window: timedelta) -> None:
        self._limit = limit
        self._window = window
        self._store: dict[str, list[datetime]] = defaultdict(list)
        self._lock = threading.Lock()

    def is_allowed(self, key: str) -> bool:
        """Return True if allowed, False if rate limit exceeded."""
        now = datetime.now(UTC)
        cutoff = now - self._window
        with self._lock:
            self._store[key] = [t for t in self._store[key] if t > cutoff]
            if len(self._store[key]) >= self._limit:
                return False
            self._store[key].append(now)
            return True
