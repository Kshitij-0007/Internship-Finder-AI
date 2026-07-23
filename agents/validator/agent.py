"""
Hermes AI OS — Validator Agent

Validates discovered job listings for relevance, freshness, and accuracy.
Assigns a confidence score and publishes JOB_VALIDATED events.
"""

import logging
from typing import Any, List

from agents.base import BaseAgent
from core.event_bus import bus
from events.events import JOB_DISCOVERED, JOB_VALIDATED
from memory.shared_memory import memory

logger = logging.getLogger("hermes.agents.validator")


class ValidatorAgent(BaseAgent):
    """Validates job listings and assigns confidence scores."""

    def __init__(self) -> None:
        super().__init__(name="validator")

    @property
    def capabilities(self) -> List[str]:
        return [JOB_DISCOVERED]

    def handle(self, payload: Any) -> None:
        """Validate a discovered job and publish JOB_VALIDATED."""
        company = payload.get("company", "Unknown")
        role = payload.get("role", "Unknown")
        self.logger.info("Validating: %s — %s", company, role)

        # Validation logic: check required fields and assign confidence
        confidence = self._calculate_confidence(payload)
        payload["confidence"] = confidence
        payload["validated"] = True

        # Update shared memory
        job_id = f"{company}_{role}"
        memory.store(job_id, payload)

        if confidence >= 50:
            bus.publish(JOB_VALIDATED, payload)
            self.logger.info("Validated (%d%% confidence): %s — %s", confidence, company, role)
        else:
            self.logger.warning(
                "Rejected (%d%% confidence): %s — %s", confidence, company, role
            )

    def _calculate_confidence(self, job: dict) -> int:
        """Score a job listing 0–100 based on completeness and quality."""
        score = 0
        if job.get("company"):
            score += 25
        if job.get("role"):
            score += 25
        if job.get("location"):
            score += 20
        if job.get("url"):
            score += 15
        if job.get("date"):
            score += 15
        return min(score, 100)
