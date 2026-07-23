"""
Hermes AI OS — Careers MCP

Reads company data from the local companies.json file and
returns structured job listings. This is the primary data source.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcps.gateway import BaseMCP

logger = logging.getLogger("hermes.mcps.careers")


class CareerMCP(BaseMCP):
    """Local careers page MCP — reads from data/companies.json."""

    name = "careers"

    def __init__(self, data_path: Optional[str] = None) -> None:
        if data_path:
            self._data_path = Path(data_path)
        else:
            self._data_path = Path(__file__).parent.parent / "data" / "companies.json"

    def fetch_all_jobs(self) -> List[Dict[str, Any]]:
        """Fetch all job listings from the companies file."""
        try:
            companies = json.loads(self._data_path.read_text(encoding="utf-8"))
            jobs = []
            for entry in companies:
                jobs.append(
                    {
                        "company": entry.get("company", "Unknown"),
                        "role": entry.get("role", "Software Engineering Intern"),
                        "location": entry.get("location", "Remote"),
                        "url": entry.get("url", ""),
                        "date": entry.get("date", ""),
                    }
                )
            logger.info("CareerMCP: loaded %d listings", len(jobs))
            return jobs
        except FileNotFoundError:
            logger.error("Companies file not found: %s", self._data_path)
            return []
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON in companies file: %s", exc)
            return []

    def fetch_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a single job by company name."""
        jobs = self.fetch_all_jobs()
        for job in jobs:
            if job.get("company", "").lower() == job_id.lower():
                return job
        return None
