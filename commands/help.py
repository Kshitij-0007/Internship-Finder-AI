"""
Hermes AI OS — Help Command

Returns help text describing available Hermes commands.
"""

HELP_TEXT = """
╔══════════════════════════════════════════════════════════════╗
║              Hermes AI Operating System — Help               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Commands:                                                   ║
║    scan [target]     Scan for internship listings            ║
║    company <name>    Look up a company's listings            ║
║    status            Show system status and health            ║
║    analytics         Generate analytics report               ║
║    help              Show this help message                  ║
║                                                              ║
║  Slack Commands:                                             ║
║    /hermes-scan      Trigger a scan from Slack               ║
║    /hermes-status    Check system status from Slack           ║
║    /hermes-analytics Generate analytics from Slack            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""


def help_text() -> str:
    """Return the Hermes help text."""
    return HELP_TEXT
