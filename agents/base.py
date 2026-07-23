"""
Hermes AI OS — Base Agent

Abstract base class that all Hermes agents must inherit from.
Ensures a consistent interface for the lifecycle manager, registry,
and dispatcher.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from core.event_bus import bus

logger = logging.getLogger("hermes.agents.base")


class BaseAgent(ABC):
    """Abstract base for every Hermes agent.

    Subclasses must implement:
        - ``handle(payload)`` — process an incoming event payload
        - ``capabilities`` (property) — list of event types this agent handles

    Optional overrides:
        - ``startup()``       — called when the agent is started
        - ``shutdown()``      — called when the agent is stopped
        - ``health_check()``  — called for health monitoring
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.logger = logging.getLogger(f"hermes.agents.{name}")

    # ── abstract interface ──────────────────────────────────────────

    @property
    @abstractmethod
    def capabilities(self) -> List[str]:
        """Event types this agent can handle."""
        ...

    @abstractmethod
    def handle(self, payload: Any) -> None:
        """Process an event payload dispatched to this agent."""
        ...

    # ── lifecycle hooks (optional overrides) ────────────────────────

    def startup(self) -> None:
        """Called once when the agent starts. Subscribe to events here."""
        for event_type in self.capabilities:
            bus.subscribe(event_type, self.handle)
        self.logger.info("Agent '%s' started — subscribed to %s", self.name, self.capabilities)

    def shutdown(self) -> None:
        """Called once when the agent is being stopped."""
        for event_type in self.capabilities:
            bus.unsubscribe(event_type, self.handle)
        self.logger.info("Agent '%s' shut down", self.name)

    def health_check(self) -> str:
        """Return health status string."""
        return "ok"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"
