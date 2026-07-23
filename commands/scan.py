"""
Hermes AI OS — Scan Command

Triggers the internship discovery pipeline through the event bus.
"""

import logging

from core.event_bus import bus
from events.events import SCAN_REQUEST

logger = logging.getLogger("hermes.commands.scan")


def run(target: str = "all") -> None:
    """Execute the scan command.

    Args:
        target: Which sources to scan ("all", or a specific MCP name).
    """
    logger.info("Scan command triggered — target: %s", target)
    bus.publish(SCAN_REQUEST, {"target": target})
