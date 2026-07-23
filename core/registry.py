"""
Hermes AI OS — Agent Registry

Dynamic capability registry. Agents register themselves with
a name and the event types they handle. The orchestrator and
dispatcher query this registry to route events to the correct agents.
"""

import logging
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("hermes.core.registry")


class AgentRecord:
    """Metadata about a registered agent."""

    def __init__(
        self,
        name: str,
        agent_instance: Any,
        capabilities: List[str],
        description: str = "",
    ) -> None:
        self.name = name
        self.agent = agent_instance
        self.capabilities = capabilities
        self.description = description
        self.is_active = True

    def __repr__(self) -> str:
        status = "active" if self.is_active else "inactive"
        return f"<AgentRecord name={self.name!r} caps={self.capabilities} {status}>"


class AgentRegistry:
    """Central registry for all agents in the Hermes AI OS.

    Agents register at startup; the dispatcher uses the registry to
    find which agents can handle a given event type.
    """

    def __init__(self) -> None:
        self._agents: Dict[str, AgentRecord] = {}

    def register(
        self,
        name: str,
        agent_instance: Any,
        capabilities: List[str],
        description: str = "",
    ) -> None:
        """Register an agent with its capabilities."""
        record = AgentRecord(name, agent_instance, capabilities, description)
        self._agents[name] = record
        logger.info("Registered agent '%s' with capabilities %s", name, capabilities)

    def unregister(self, name: str) -> None:
        """Remove an agent from the registry."""
        if name in self._agents:
            del self._agents[name]
            logger.info("Unregistered agent '%s'", name)

    def get(self, name: str) -> Optional[AgentRecord]:
        """Look up an agent by name."""
        return self._agents.get(name)

    def find_by_capability(self, event_type: str) -> List[AgentRecord]:
        """Return all active agents that declare *event_type* as a capability."""
        return [
            record
            for record in self._agents.values()
            if record.is_active and event_type in record.capabilities
        ]

    def list_agents(self) -> List[AgentRecord]:
        """Return all registered agents."""
        return list(self._agents.values())

    def set_active(self, name: str, active: bool) -> None:
        """Enable or disable an agent without removing it."""
        record = self._agents.get(name)
        if record:
            record.is_active = active
            state = "activated" if active else "deactivated"
            logger.info("Agent '%s' %s", name, state)


# ── module-level singleton ──────────────────────────────────────────
registry = AgentRegistry()
