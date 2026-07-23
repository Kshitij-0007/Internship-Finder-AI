"""
Hermes AI OS — Duplicate Detection Agent

Detects and deduplicates job listings to prevent the same internship
from being published multiple times. Listens for JOB_DISCOVERED events.
"""

import logging
from typing import Any, Dict, List, Set

from agents.base import BaseAgent
from core.event_bus import bus
from events.events import JOB_DISCOVERED, DUPLICATE_DETECTED
from memory.shared_memory import memory

logger = logging.getLogger("hermes.agents.duplicate")


class DuplicateAgent(BaseAgent):
    """Detects duplicate internship listings."""

    def __init__(self) -> None:
        super().__init__(name="duplicate")
        self._seen_signatures: Set[str] = set()

    @property
    def capabilities(self) -> List[str]:
        return [JOB_DISCOVERED]

    def handle(self, payload: Any) -> None:
        """Check if a discovered job is a duplicate."""
        signature = self._compute_signature(payload)
        company = payload.get("company", "Unknown")
        role = payload.get("role", "Unknown")

        if signature in self._seen_signatures:
            self.logger.warning("Duplicate detected: %s — %s", company, role)
            payload["is_duplicate"] = True
            bus.publish(DUPLICATE_DETECTED, payload)
        else:
            self._seen_signatures.add(signature)
            payload["is_duplicate"] = False
            self.logger.info("New listing registered: %s — %s", company, role)

    def _compute_signature(self, job: dict) -> str:
        """Create a unique signature for a job listing."""
        company = (job.get("company") or "").lower().strip()
        role = (job.get("role") or "").lower().strip()
        location = (job.get("location") or "").lower().strip()
        return f"{company}|{role}|{location}"

    @property
    def seen_count(self) -> int:
        return len(self._seen_signatures)

    def reset(self) -> None:
        """Clear the duplicate cache."""
        self._seen_signatures.clear()
