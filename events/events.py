"""
Hermes AI OS — Event Types

Central registry of all event types used across the system.
Agents subscribe to these events through the core event bus.
"""

# ── Discovery Pipeline ─────────────────────────────────────────────
SCAN_REQUEST = "SCAN_REQUEST"
JOB_DISCOVERED = "JOB_DISCOVERED"
JOB_VALIDATED = "JOB_VALIDATED"
JOB_PUBLISHED = "JOB_PUBLISHED"

# ── Ranking & Salary ───────────────────────────────────────────────
JOB_RANKED = "JOB_RANKED"
SALARY_ESTIMATED = "SALARY_ESTIMATED"

# ── Duplicate Detection ────────────────────────────────────────────
DUPLICATE_DETECTED = "DUPLICATE_DETECTED"

# ── Analytics ──────────────────────────────────────────────────────
ANALYTICS_REQUEST = "ANALYTICS_REQUEST"
ANALYTICS_READY = "ANALYTICS_READY"

# ── System Events ──────────────────────────────────────────────────
STATUS_REQUEST = "STATUS_REQUEST"
SYSTEM_BOOT = "SYSTEM_BOOT"
SYSTEM_SHUTDOWN = "SYSTEM_SHUTDOWN"
AGENT_REGISTERED = "AGENT_REGISTERED"
AGENT_ERROR = "AGENT_ERROR"

# ── Slack Events ───────────────────────────────────────────────────
SLACK_COMMAND = "SLACK_COMMAND"
SLACK_MESSAGE = "SLACK_MESSAGE"
