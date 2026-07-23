"""
Hermes AI OS — Prompt Templates

Central repository of prompt templates used by agents when
interacting with AI providers. Organized by agent and task.
"""

# ── System-wide prompts ────────────────────────────────────────────

HERMES_SYSTEM_PROMPT = """You are Hermes, an AI Operating System that orchestrates
multiple specialized agents to discover, validate, rank, and publish
internship opportunities. You communicate through an event-driven architecture.
"""

# ── Re-export agent-specific prompts for convenience ───────────────

from agents.scout.prompts import SCOUT_SYSTEM_PROMPT, SCOUT_EXTRACT_PROMPT
from agents.validator.prompts import VALIDATOR_SYSTEM_PROMPT, VALIDATOR_CHECK_PROMPT
from agents.publisher.prompts import PUBLISHER_SYSTEM_PROMPT, PUBLISHER_FORMAT_PROMPT
from agents.ranking.prompts import RANKING_SYSTEM_PROMPT, RANKING_EVALUATE_PROMPT
from agents.salary.prompts import SALARY_SYSTEM_PROMPT, SALARY_ESTIMATE_PROMPT
from agents.duplicate.prompts import DUPLICATE_SYSTEM_PROMPT, DUPLICATE_CHECK_PROMPT
from agents.analytics.prompts import ANALYTICS_SYSTEM_PROMPT, ANALYTICS_REPORT_PROMPT

__all__ = [
    "HERMES_SYSTEM_PROMPT",
    "SCOUT_SYSTEM_PROMPT",
    "SCOUT_EXTRACT_PROMPT",
    "VALIDATOR_SYSTEM_PROMPT",
    "VALIDATOR_CHECK_PROMPT",
    "PUBLISHER_SYSTEM_PROMPT",
    "PUBLISHER_FORMAT_PROMPT",
    "RANKING_SYSTEM_PROMPT",
    "RANKING_EVALUATE_PROMPT",
    "SALARY_SYSTEM_PROMPT",
    "SALARY_ESTIMATE_PROMPT",
    "DUPLICATE_SYSTEM_PROMPT",
    "DUPLICATE_CHECK_PROMPT",
    "ANALYTICS_SYSTEM_PROMPT",
    "ANALYTICS_REPORT_PROMPT",
]
