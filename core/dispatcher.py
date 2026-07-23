"""
Hermes AI OS — Dispatcher

Routes events from the bus to the correct agents via the registry.
Sits between the event bus and the agents: when an event fires, the
dispatcher looks up which agents declared that event as a capability
and forwards the payload to each.
"""

import logging
from typing import Any

from core.event_bus import bus
from core.registry import registry

logger = logging.getLogger("hermes.core.dispatcher")


class Dispatcher:
    """Event-to-agent dispatcher.

    Subscribes to all events ("*") on the bus and forwards each event
    to every agent that registered the matching capability.
    """

    def __init__(self) -> None:
        self._enabled = False

    def start(self) -> None:
        """Activate the dispatcher by subscribing to the wildcard channel."""
        if not self._enabled:
            bus.subscribe("*", self._route)
            self._enabled = True
            logger.info("Dispatcher started — listening for all events")

    def stop(self) -> None:
        """Deactivate the dispatcher."""
        if self._enabled:
            bus.unsubscribe("*", self._route)
            self._enabled = False
            logger.info("Dispatcher stopped")

    def _route(self, payload: Any) -> None:
        """Internal handler invoked on every event; forwards to matching agents."""
        # The event_type is stored in the latest event log entry
        event_log = bus.event_log
        if not event_log:
            return

        event_type = event_log[-1]["event"]
        agents = registry.find_by_capability(event_type)

        if not agents:
            logger.debug("No agents registered for event '%s'", event_type)
            return

        for record in agents:
            agent = record.agent
            handler = getattr(agent, "handle", None)
            if callable(handler):
                try:
                    handler(payload)
                    logger.info(
                        "Dispatched '%s' to agent '%s'", event_type, record.name
                    )
                except Exception as exc:
                    logger.error(
                        "Agent '%s' failed handling '%s': %s",
                        record.name,
                        event_type,
                        exc,
                    )


# ── module-level singleton ──────────────────────────────────────────
dispatcher = Dispatcher()
