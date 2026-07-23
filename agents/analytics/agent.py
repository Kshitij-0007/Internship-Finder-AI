"""
Hermes AI OS — Analytics Agent

Generates analytics and insights from job discovery data.
Listens for JOB_PUBLISHED events and publishes ANALYTICS_READY events.
Also responds to ANALYTICS_REQUEST for on-demand reports.
"""

import logging
from collections import Counter
from typing import Any, Dict, List

from agents.base import BaseAgent
from core.event_bus import bus
from events.events import JOB_PUBLISHED, ANALYTICS_REQUEST, ANALYTICS_READY
from memory.shared_memory import memory

logger = logging.getLogger("hermes.agents.analytics")


class AnalyticsAgent(BaseAgent):
    """Generates analytics and insights from internship data."""

    def __init__(self) -> None:
        super().__init__(name="analytics")
        self._published_jobs: List[Dict[str, Any]] = []

    @property
    def capabilities(self) -> List[str]:
        return [JOB_PUBLISHED, ANALYTICS_REQUEST]

    def handle(self, payload: Any) -> None:
        """Track published jobs or generate analytics report."""
        if payload.get("published"):
            self._track_job(payload)
        else:
            self._generate_report()

    def _track_job(self, job: dict) -> None:
        """Track a published job for analytics."""
        self._published_jobs.append(job)
        self.logger.info(
            "Tracking job %s — %s (total: %d)",
            job.get("company"),
            job.get("role"),
            len(self._published_jobs),
        )

    def _generate_report(self) -> None:
        """Generate and publish an analytics report."""
        if not self._published_jobs:
            self.logger.info("No data available for analytics report")
            report = {"total_jobs": 0, "message": "No jobs discovered yet"}
            bus.publish(ANALYTICS_READY, report)
            return

        companies = Counter(j.get("company", "Unknown") for j in self._published_jobs)
        locations = Counter(j.get("location", "N/A") for j in self._published_jobs)
        confidences = [j.get("confidence", 0) for j in self._published_jobs]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        report = {
            "total_jobs": len(self._published_jobs),
            "companies": dict(companies.most_common(10)),
            "locations": dict(locations.most_common(10)),
            "avg_confidence": round(avg_confidence, 1),
        }

        self.logger.info("Analytics report generated: %d total jobs", report["total_jobs"])
        output = (
            f"\n[Analytics Report]\n"
            f"   Total jobs:       {report['total_jobs']}\n"
            f"   Avg confidence:   {report['avg_confidence']}%\n"
            f"   Top companies:    {report['companies']}\n"
            f"   Top locations:    {report['locations']}\n"
        )
        try:
            print(output)
        except UnicodeEncodeError:
            print(output.encode("ascii", "replace").decode("ascii"))

        bus.publish(ANALYTICS_READY, report)
