"""
Hermes AI OS — Publisher Agent

Publishes validated internship listings to configured output channels
(Slack, console, etc.). Final step in the discovery pipeline.
"""

import logging
import sys
from typing import Any, List

from agents.base import BaseAgent
from core.event_bus import bus
from events.events import JOB_VALIDATED, JOB_PUBLISHED
from memory.shared_memory import memory

logger = logging.getLogger("hermes.agents.publisher")


class PublisherAgent(BaseAgent):
    """Publishes validated job listings to output channels."""

    def __init__(self) -> None:
        super().__init__(name="publisher")
        self._published_count = 0

    @property
    def capabilities(self) -> List[str]:
        return [JOB_VALIDATED]

    def handle(self, payload: Any) -> None:
        """Publish a validated job listing."""
        company = payload.get("company", "Unknown")
        role = payload.get("role", "Unknown")
        location = payload.get("location", "N/A")
        confidence = payload.get("confidence", 0)

        # Format the output safely for Windows console encoding
        message = (
            f"[New Internship Listing]\n"
            f"   Company:    {company}\n"
            f"   Role:       {role}\n"
            f"   Location:   {location}\n"
            f"   Confidence: {confidence}%\n"
        )
        try:
            print(message)
        except UnicodeEncodeError:
            print(message.encode("ascii", "replace").decode("ascii"))

        self.logger.info("Published: %s — %s (%d%%)", company, role, confidence)

        self._published_count += 1
        payload["published"] = True

        # Update memory and emit completion event
        job_id = f"{company}_{role}"
        memory.store(job_id, payload)
        bus.publish(JOB_PUBLISHED, payload)

    @property
    def published_count(self) -> int:
        return self._published_count
