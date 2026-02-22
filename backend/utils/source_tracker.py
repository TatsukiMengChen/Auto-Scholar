"""Simple failure tracking for data sources.

Tracks recent failures per source and skips sources that fail repeatedly
within a time window. Not a full circuit breaker - just failure counting.
"""

import time

from backend.constants import SOURCE_SKIP_THRESHOLD, SOURCE_SKIP_WINDOW_SECONDS

_failures: dict[str, list[float]] = {}


def should_skip(source: str) -> bool:
    """Check if source should be skipped due to recent failures."""
    now = time.time()
    times = _failures.get(source, [])
    recent = [t for t in times if now - t < SOURCE_SKIP_WINDOW_SECONDS]
    _failures[source] = recent
    return len(recent) >= SOURCE_SKIP_THRESHOLD


def record_failure(source: str) -> None:
    """Record a failure for the given source."""
    _failures.setdefault(source, []).append(time.time())


def record_success(source: str) -> None:
    """Clear failure history on success."""
    _failures.pop(source, None)


def reset_all() -> None:
    """Reset all failure tracking. Useful for testing."""
    _failures.clear()
