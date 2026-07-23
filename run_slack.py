"""
Hermes AI OS — Slack Mission Control Runner

Boots the Hermes AI Operating System orchestrator and connects
it to your Slack workspace using Socket Mode.
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

from slack.bot import HermesSlackBot
from services.logger import setup_logging
from config.settings import LOG_LEVEL, LOG_FILE


def main():
    print("=" * 60)
    print("  Hermes AI OS — Slack Mission Control")
    print("=" * 60)

    # 1. Setup logging
    setup_logging(level=LOG_LEVEL, log_file=LOG_FILE)

    # 2. Setup MCP Gateway
    gateway = MCPGateway()
    gateway.register(CareerMCP())
    gateway.register(GreenhouseMCP())
    gateway.register(LeverMCP())
    gateway.register(AshbyMCP())

    # 3. Create Orchestrator and register all agents
    hermes = Orchestrator()

    hermes.lifecycle.register_agent(
        name="scout",
        factory=ScoutAgent,
        capabilities=["SCAN_REQUEST"],
        description="Discovers internship listings from MCP connectors",
        mcp=gateway,
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

    # 4. Boot Orchestrator
    hermes.boot()

    # 5. Connect and start Slack Bot
    print("\n[+] Connecting to Slack Socket Mode...")
    slack_bot = HermesSlackBot()
    try:
        slack_bot.start()
    except KeyboardInterrupt:
        print("\nStopping Slack bot...")
        slack_bot.stop()
        hermes.shutdown()


if __name__ == "__main__":
    main()
