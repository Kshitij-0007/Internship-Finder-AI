"""
Hermes AI OS — Status Command

Returns the current system status, agent health, and memory stats.
"""

import logging
from typing import Any, Dict

from core.registry import registry
from core.lifecycle import LifecycleManager
from memory.shared_memory import memory

logger = logging.getLogger("hermes.commands.status")


def status(lifecycle: LifecycleManager = None) -> Dict[str, Any]:
    """Return the current system status.

    Returns:
        Dict with agent statuses, memory stats, and health checks.
    """
    agents = registry.list_agents()
    agent_info = []
    for record in agents:
        agent_info.append({
            "name": record.name,
            "active": record.is_active,
            "capabilities": record.capabilities,
        })

    health = {}
    if lifecycle:
        health = lifecycle.health_check()

    result = {
        "status": "running",
        "agents": agent_info,
        "agent_count": len(agents),
        "memory_entries": memory.count(),
        "health": health,
    }

    logger.info("Status: %d agents, %d memory entries", len(agents), memory.count())
    return result
