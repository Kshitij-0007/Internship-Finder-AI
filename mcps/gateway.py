"""
Hermes AI OS — MCP Gateway

Unified gateway that aggregates job listings from all registered
MCP connectors (careers pages, Greenhouse, Lever, Ashby, etc.).
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("hermes.mcps.gateway")


class BaseMCP:
    """Interface that every MCP connector must implement."""

    name: str = "base"

    def fetch_all_jobs(self) -> List[Dict[str, Any]]:
        """Fetch all available job listings."""
        raise NotImplementedError

    def fetch_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a single job by ID."""
        raise NotImplementedError


class MCPGateway:
    """Aggregating gateway over multiple MCP connectors.

    Usage::

        gateway = MCPGateway()
        gateway.register(CareerMCP())
        gateway.register(GreenhouseMCP())
        jobs = gateway.fetch_all_jobs()
    """

    def __init__(self) -> None:
        self._connectors: Dict[str, BaseMCP] = {}

    def register(self, connector: BaseMCP) -> None:
        """Register an MCP connector with the gateway."""
        self._connectors[connector.name] = connector
        logger.info("Registered MCP connector: %s", connector.name)

    def unregister(self, name: str) -> None:
        """Remove an MCP connector."""
        if name in self._connectors:
            del self._connectors[name]
            logger.info("Unregistered MCP connector: %s", name)

    def fetch_all_jobs(self) -> List[Dict[str, Any]]:
        """Aggregate job listings from all registered connectors."""
        all_jobs: List[Dict[str, Any]] = []

        for name, connector in self._connectors.items():
            try:
                jobs = connector.fetch_all_jobs()
                # Tag each job with its source
                for job in jobs:
                    job["source"] = name
                all_jobs.extend(jobs)
                logger.info("Fetched %d jobs from %s", len(jobs), name)
            except Exception as exc:
                logger.error("Failed to fetch from %s: %s", name, exc)

        logger.info("Gateway total: %d jobs from %d sources", len(all_jobs), len(self._connectors))
        return all_jobs

    def list_connectors(self) -> List[str]:
        """Return the names of all registered connectors."""
        return list(self._connectors.keys())
