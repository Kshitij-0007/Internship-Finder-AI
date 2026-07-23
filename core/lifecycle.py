"""
Hermes AI OS — Lifecycle Manager

Manages the full lifecycle of agents: discovery, registration,
startup, health checks, and shutdown.
"""

import logging
from typing import Any, Dict, List, Optional

from core.event_bus import bus
from core.registry import registry

logger = logging.getLogger("hermes.core.lifecycle")


class LifecycleManager:
    """Manages agent lifecycle: registration, start, stop, health."""

    def __init__(self) -> None:
        self._agent_factories: List[Dict[str, Any]] = []
        self._started = False

    def register_agent(
        self,
        name: str,
        factory: Any,
        capabilities: List[str],
        description: str = "",
        **kwargs: Any,
    ) -> None:
        """Queue an agent factory for startup.

        Args:
            name: Unique agent name.
            factory: Callable / class that produces the agent instance.
            capabilities: Event types this agent handles.
            description: Human-readable description.
            **kwargs: Extra keyword arguments forwarded to the factory.
        """
        self._agent_factories.append(
            {
                "name": name,
                "factory": factory,
                "capabilities": capabilities,
                "description": description,
                "kwargs": kwargs,
            }
        )
        logger.info("Queued agent '%s' for registration", name)

    def start_all(self) -> None:
        """Instantiate and register every queued agent."""
        if self._started:
            logger.warning("Lifecycle manager already started")
            return

        for entry in self._agent_factories:
            try:
                instance = entry["factory"](**entry["kwargs"])
                registry.register(
                    name=entry["name"],
                    agent_instance=instance,
                    capabilities=entry["capabilities"],
                    description=entry["description"],
                )
                logger.info("Agent '%s' started successfully", entry["name"])
            except Exception as exc:
                logger.error("Failed to start agent '%s': %s", entry["name"], exc)

        self._started = True

    def stop_all(self) -> None:
        """Gracefully stop all agents."""
        for record in registry.list_agents():
            agent = record.agent
            shutdown = getattr(agent, "shutdown", None)
            if callable(shutdown):
                try:
                    shutdown()
                except Exception as exc:
                    logger.error("Error shutting down '%s': %s", record.name, exc)
            registry.set_active(record.name, False)
            logger.info("Agent '%s' stopped", record.name)

        self._started = False

    def health_check(self) -> Dict[str, str]:
        """Return a map of agent_name -> health status."""
        results: Dict[str, str] = {}
        for record in registry.list_agents():
            agent = record.agent
            check = getattr(agent, "health_check", None)
            if callable(check):
                try:
                    results[record.name] = check()
                except Exception:
                    results[record.name] = "error"
            else:
                results[record.name] = "ok" if record.is_active else "inactive"
        return results
