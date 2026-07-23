"""
Hermes AI OS — Salary Agent

Estimates salary and compensation data for internship listings.
Listens for JOB_VALIDATED events and publishes SALARY_ESTIMATED events.
"""

import logging
from typing import Any, Dict, List

from agents.base import BaseAgent
from core.event_bus import bus
from events.events import JOB_VALIDATED, SALARY_ESTIMATED
from memory.shared_memory import memory

logger = logging.getLogger("hermes.agents.salary")

# Estimated salary ranges by company tier (monthly, USD)
SALARY_ESTIMATES: Dict[str, Dict[str, int]] = {
    "tier1": {"min": 6000, "max": 12000},   # FAANG / top-tier
    "tier2": {"min": 3500, "max": 6000},     # Large tech
    "tier3": {"min": 1500, "max": 3500},     # Mid-size / startups
    "default": {"min": 1000, "max": 3000},
}

TIER1_COMPANIES = {"google", "microsoft", "apple", "meta", "amazon", "netflix"}
TIER2_COMPANIES = {"oracle", "ibm", "mastercard", "salesforce", "adobe", "intuit"}


class SalaryAgent(BaseAgent):
    """Estimates salary / compensation for internship listings."""

    def __init__(self) -> None:
        super().__init__(name="salary")

    @property
    def capabilities(self) -> List[str]:
        return [JOB_VALIDATED]

    def handle(self, payload: Any) -> None:
        """Estimate salary for a validated job listing."""
        company = payload.get("company", "Unknown")
        role = payload.get("role", "Unknown")
        self.logger.info("Estimating salary: %s — %s", company, role)

        estimate = self._estimate_salary(company)
        payload["salary_estimate"] = estimate

        job_id = f"{company}_{role}"
        memory.store(job_id, payload)

        bus.publish(SALARY_ESTIMATED, payload)
        self.logger.info(
            "Salary estimate for %s: $%d–$%d/month",
            company,
            estimate["min"],
            estimate["max"],
        )

    def _estimate_salary(self, company: str) -> Dict[str, int]:
        """Return a salary range estimate based on company tier."""
        company_lower = company.lower()
        if company_lower in TIER1_COMPANIES:
            return dict(SALARY_ESTIMATES["tier1"])
        elif company_lower in TIER2_COMPANIES:
            return dict(SALARY_ESTIMATES["tier2"])
        else:
            return dict(SALARY_ESTIMATES["default"])
