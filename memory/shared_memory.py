"""
Hermes AI OS — Shared Memory

Thread-safe shared state store for the entire system. All agents
read and write job data through this centralized memory.
"""

import json
import logging
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("hermes.memory")


class SharedMemory:
    """Thread-safe in-memory store with optional persistence.

    Stores job data keyed by job_id. Supports snapshots to disk
    for crash recovery.
    """

    def __init__(self, persist_path: Optional[str] = None) -> None:
        self._data: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self._persist_path = Path(persist_path) if persist_path else None

        # Load from disk if available
        if self._persist_path and self._persist_path.exists():
            try:
                self._data = json.loads(self._persist_path.read_text(encoding="utf-8"))
                logger.info("Loaded %d entries from %s", len(self._data), self._persist_path)
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Could not load persisted memory: %s", exc)

    def store(self, key: str, value: Any) -> None:
        """Store a value by key (thread-safe)."""
        with self._lock:
            self._data[key] = value
            logger.debug("Stored key: %s", key)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value by key."""
        with self._lock:
            return self._data.get(key, default)

    def exists(self, key: str) -> bool:
        """Check if a key exists."""
        with self._lock:
            return key in self._data

    def delete(self, key: str) -> None:
        """Remove a key."""
        with self._lock:
            self._data.pop(key, None)

    def list_keys(self) -> List[str]:
        """Return all stored keys."""
        with self._lock:
            return list(self._data.keys())

    def count(self) -> int:
        """Return the number of stored entries."""
        with self._lock:
            return len(self._data)

    def get_all(self) -> Dict[str, Any]:
        """Return a shallow copy of all stored data."""
        with self._lock:
            return dict(self._data)

    def clear(self) -> None:
        """Remove all entries."""
        with self._lock:
            self._data.clear()
            logger.info("Memory cleared")

    def persist(self) -> None:
        """Snapshot current state to disk."""
        if not self._persist_path:
            logger.debug("No persist path configured, skipping")
            return
        with self._lock:
            self._persist_path.parent.mkdir(parents=True, exist_ok=True)
            self._persist_path.write_text(
                json.dumps(self._data, indent=2, default=str),
                encoding="utf-8",
            )
            logger.info("Persisted %d entries to %s", len(self._data), self._persist_path)


# ── module-level singleton ──────────────────────────────────────────
memory = SharedMemory()
