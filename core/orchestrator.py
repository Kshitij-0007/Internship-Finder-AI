"""
Hermes AI OS — Orchestrator

The central Hermes orchestrator. It is the brain of the system:
- Boots all agents through the lifecycle manager
- Starts the dispatcher
- Provides the high-level API to trigger workflows

Workflow:
    Slack -> Hermes -> Dispatcher -> Event Bus -> Agents -> Memory -> Publisher -> Slack
"""

import logging
from typing import Any, Dict, Optional

from core.event_bus import bus
from core.registry import registry
from core.dispatcher import dispatcher
from core.lifecycle import LifecycleManager

logger = logging.getLogger("hermes.core.orchestrator")


class Orchestrator:
    """Hermes — the AI Operating System orchestrator.

    Usage::

        hermes = Orchestrator()
        hermes.boot()            # registers agents, starts dispatcher
        hermes.run("scan")       # triggers a workflow by name
        hermes.shutdown()        # graceful teardown
    """

    def __init__(self) -> None:
        self.lifecycle = LifecycleManager()
        self._workflows: Dict[str, str] = {
            "scan": "SCAN_REQUEST",
            "status": "STATUS_REQUEST",
            "analytics": "ANALYTICS_REQUEST",
        }
        self._booted = False

    def boot(self) -> None:
        """Initialize the runtime: register agents, start dispatcher."""
        if self._booted:
            logger.warning("Orchestrator already booted")
            return

        logger.info("=" * 60)
        logger.info("  Hermes AI Operating System — Booting")
        logger.info("=" * 60)

        # 1. Start the lifecycle manager (registers and starts all agents)
        self.lifecycle.start_all()

        # 2. Start the dispatcher
        dispatcher.start()

        self._booted = True
        agents = registry.list_agents()
        logger.info(
            "Boot complete — %d agent(s) registered: %s",
            len(agents),
            [a.name for a in agents],
        )

    def run(self, workflow: str, payload: Optional[Dict[str, Any]] = None) -> None:
        """Trigger a named workflow by publishing its initiating event."""
        if not self._booted:
            logger.error("Cannot run workflow '%s' — orchestrator not booted", workflow)
            return

        event = self._workflows.get(workflow)
        if not event:
            logger.error("Unknown workflow: '%s'", workflow)
            return

        logger.info("Running workflow '%s' -> event '%s'", workflow, event)
        bus.publish(event, payload or {})

    def register_workflow(self, name: str, event_type: str) -> None:
        """Register a custom workflow name -> event mapping."""
        self._workflows[name] = event_type

    def shutdown(self) -> None:
        """Graceful shutdown: stop dispatcher, tear down agents."""
        logger.info("Hermes shutting down...")
        dispatcher.stop()
        self.lifecycle.stop_all()
        self._booted = False
        logger.info("Hermes shutdown complete")
