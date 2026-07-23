"""
Hermes AI OS — Event Bus

Async-capable event bus with logging, retry support, and wildcard
subscriptions. All agent communication flows through this bus;
agents never call each other directly.
"""

import asyncio
import logging
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("hermes.core.event_bus")


class EventBus:
    """Central event bus for the Hermes AI Operating System.

    Supports synchronous and asynchronous handlers, wildcard
    subscriptions ("*"), and optional retry on handler failure.
    """

    def __init__(self, max_retries: int = 2) -> None:
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._max_retries = max_retries
        self._event_log: List[Dict[str, Any]] = []

    # ── subscription ────────────────────────────────────────────────

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Register *handler* to be called when *event_type* is published."""
        self._subscribers[event_type].append(handler)
        logger.info("Subscribed %s to event '%s'", handler.__qualname__, event_type)

    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Remove *handler* from *event_type*."""
        handlers = self._subscribers.get(event_type, [])
        if handler in handlers:
            handlers.remove(handler)
            logger.info("Unsubscribed %s from '%s'", handler.__qualname__, event_type)

    # ── publishing (sync) ───────────────────────────────────────────

    def publish(self, event_type: str, payload: Any = None) -> None:
        """Publish an event synchronously. Handlers run in order."""
        self._event_log.append({"event": event_type, "payload": payload})
        logger.info("Publishing event '%s'", event_type)

        handlers = list(self._subscribers.get(event_type, []))
        # wildcard listeners
        handlers.extend(self._subscribers.get("*", []))

        for handler in handlers:
            self._invoke_with_retry(handler, payload)

    def _invoke_with_retry(self, handler: Callable, payload: Any) -> None:
        """Invoke a single handler with retry logic."""
        for attempt in range(1, self._max_retries + 1):
            try:
                handler(payload)
                return
            except Exception as exc:
                logger.warning(
                    "Handler %s failed (attempt %d/%d): %s",
                    handler.__qualname__,
                    attempt,
                    self._max_retries,
                    exc,
                )
        logger.error(
            "Handler %s exhausted retries for event payload: %s",
            handler.__qualname__,
            payload,
        )

    # ── publishing (async) ──────────────────────────────────────────

    async def publish_async(self, event_type: str, payload: Any = None) -> None:
        """Publish an event asynchronously."""
        self._event_log.append({"event": event_type, "payload": payload})
        logger.info("Async-publishing event '%s'", event_type)

        handlers = list(self._subscribers.get(event_type, []))
        handlers.extend(self._subscribers.get("*", []))

        tasks = []
        for handler in handlers:
            if asyncio.iscoroutinefunction(handler):
                tasks.append(handler(payload))
            else:
                handler(payload)

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    # ── introspection ───────────────────────────────────────────────

    @property
    def event_log(self) -> List[Dict[str, Any]]:
        """Return a copy of the event log."""
        return list(self._event_log)

    def list_subscriptions(self) -> Dict[str, List[str]]:
        """Return a map of event_type → list of handler names."""
        return {
            event: [h.__qualname__ for h in handlers]
            for event, handlers in self._subscribers.items()
        }

    def clear(self) -> None:
        """Remove all subscribers and clear the event log."""
        self._subscribers.clear()
        self._event_log.clear()


# ── module-level singleton ──────────────────────────────────────────
bus = EventBus()
