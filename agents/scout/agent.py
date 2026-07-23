"""
Hermes AI OS — Scout Agent

Scans career pages and job boards for internship listings.
Publishes a JOB_DISCOVERED event for each listing found.
"""

import logging
from typing import Any, List

from agents.base import BaseAgent
from core.event_bus import bus
from events.events import SCAN_REQUEST, JOB_DISCOVERED
from memory.shared_memory import memory

logger = logging.getLogger("hermes.agents.scout")


class ScoutAgent(BaseAgent):
    """Discovers internship listings from configured MCP sources."""

    def __init__(self, mcp=None) -> None:
        super().__init__(name="scout")
        self.mcp = mcp

    @property
    def capabilities(self) -> List[str]:
        return [SCAN_REQUEST]

    def handle(self, payload: Any) -> None:
        """Fetch all jobs from the MCP and publish each as JOB_DISCOVERED."""
        self.logger.info("Scout scanning for internships...")

        if self.mcp is None:
            self.logger.warning("No MCP configured for Scout agent")
            return

        jobs = self.mcp.fetch_all_jobs()
        self.logger.info("Found %d job listing(s)", len(jobs))

        for job in jobs:
            job_id = f"{job.get('company', 'unknown')}_{job.get('role', 'unknown')}"
            memory.store(job_id, job)
            bus.publish(JOB_DISCOVERED, job)

        self.logger.info("Scout scan complete — published %d events", len(jobs))
