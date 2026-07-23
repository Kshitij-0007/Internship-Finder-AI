"""
Hermes AI OS — Ranking Agent

Ranks validated internship listings by relevance, fit, and desirability.
Listens for JOB_VALIDATED events and publishes JOB_RANKED events.
"""

import logging
from typing import Any, List

from agents.base import BaseAgent
from core.event_bus import bus
from events.events import JOB_VALIDATED, JOB_RANKED
from memory.shared_memory import memory

logger = logging.getLogger("hermes.agents.ranking")


class RankingAgent(BaseAgent):
    """Ranks internship listings by relevance and fit."""

    def __init__(self) -> None:
        super().__init__(name="ranking")

    @property
    def capabilities(self) -> List[str]:
        return [JOB_VALIDATED]

    def handle(self, payload: Any) -> None:
        """Rank a validated job listing."""
        company = payload.get("company", "Unknown")
        role = payload.get("role", "Unknown")
        self.logger.info("Ranking: %s — %s", company, role)

        rank_score = self._compute_rank(payload)
        payload["rank_score"] = rank_score

        # Update memory
        job_id = f"{company}_{role}"
        memory.store(job_id, payload)

        bus.publish(JOB_RANKED, payload)
        self.logger.info("Ranked %s — %s with score %d", company, role, rank_score)

    def _compute_rank(self, job: dict) -> int:
        """Compute a ranking score 0–100 based on multiple signals."""
        score = 0

        # Confidence from validator
        confidence = job.get("confidence", 0)
        score += int(confidence * 0.4)

        # Prefer remote positions
        location = (job.get("location") or "").lower()
        if "remote" in location:
            score += 20
        elif "hybrid" in location:
            score += 10

        # Known top-tier companies get a boost
        top_companies = {"google", "microsoft", "apple", "meta", "amazon", "oracle", "ibm"}
        if job.get("company", "").lower() in top_companies:
            score += 20

        # Completeness bonus
        if job.get("url"):
            score += 10
        if job.get("date"):
            score += 10

        return min(score, 100)
