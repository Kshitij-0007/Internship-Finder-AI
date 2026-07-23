"""
Hermes AI Operating System — Entry Point

Event-driven multi-agent orchestrator for internship discovery and career management.
"""

import sys
from core.orchestrator import Orchestrator
from mcps.gateway import MCPGateway
from mcps.careers import CareerMCP
from mcps.greenhouse import GreenhouseMCP
from mcps.lever import LeverMCP
from mcps.ashby import AshbyMCP

from agents.scout.agent import ScoutAgent
from agents.validator.agent import ValidatorAgent
from agents.publisher.agent import PublisherAgent
from agents.ranking.agent import RankingAgent
from agents.salary.agent import SalaryAgent
from agents.duplicate.agent import DuplicateAgent
from agents.analytics.agent import AnalyticsAgent

from services.logger import setup_logging
from config.settings import LOG_LEVEL, LOG_FILE


def main():
    # Setup structured logging
    setup_logging(level=LOG_LEVEL, log_file=LOG_FILE)

    # Setup MCP Gateway with all job board connectors
    mcp_gateway = MCPGateway()
    mcp_gateway.register(CareerMCP())
    mcp_gateway.register(GreenhouseMCP())
    mcp_gateway.register(LeverMCP())
    mcp_gateway.register(AshbyMCP())

    # Create Orchestrator
    hermes = Orchestrator()

    # Register Agents with Lifecycle Manager
    hermes.lifecycle.register_agent(
        name="scout",
        factory=ScoutAgent,
        capabilities=["SCAN_REQUEST"],
        description="Discovers internship listings from MCP connectors",
        mcp=mcp_gateway,
    )
    hermes.lifecycle.register_agent(
        name="duplicate",
        factory=DuplicateAgent,
        capabilities=["JOB_DISCOVERED"],
        description="Detects and deduplicates job listings",
    )
    hermes.lifecycle.register_agent(
        name="validator",
        factory=ValidatorAgent,
        capabilities=["JOB_DISCOVERED"],
        description="Validates job listings for completeness and quality",
    )
    hermes.lifecycle.register_agent(
        name="ranking",
        factory=RankingAgent,
        capabilities=["JOB_VALIDATED"],
        description="Ranks job listings by relevance and fit",
    )
    hermes.lifecycle.register_agent(
        name="salary",
        factory=SalaryAgent,
        capabilities=["JOB_VALIDATED"],
        description="Estimates compensation data for job listings",
    )
    hermes.lifecycle.register_agent(
        name="analytics",
        factory=AnalyticsAgent,
        capabilities=["JOB_PUBLISHED", "ANALYTICS_REQUEST"],
        description="Tracks job metrics and generates analytics reports",
    )
    hermes.lifecycle.register_agent(
        name="publisher",
        factory=PublisherAgent,
        capabilities=["JOB_VALIDATED"],
        description="Publishes validated job listings to output channels",
    )

    # Boot system
    hermes.boot()

    # Trigger default scan workflow
    print("\n--- Running Hermes AI OS Scan Workflow ---")
    hermes.run("scan")

    # Run analytics report workflow
    print("\n--- Running Hermes Analytics Workflow ---")
    hermes.run("analytics")

    # Graceful shutdown
    hermes.shutdown()


if __name__ == "__main__":
    main()
