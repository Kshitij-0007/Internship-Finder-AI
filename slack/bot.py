"""
Hermes AI OS — Slack Bot (Mission Control)

Slack integration using Bolt framework. Slack serves as the
control plane for the Hermes AI Operating System.
"""

import logging
import os
from typing import Any, Optional

from core.event_bus import bus
from events.events import SCAN_REQUEST, ANALYTICS_REQUEST, STATUS_REQUEST, SLACK_COMMAND

logger = logging.getLogger("hermes.slack")


class HermesSlackBot:
    """Slack mission control for the Hermes AI OS.

    Handles slash commands and messages from Slack, translates
    them into events on the bus.
    """

    def __init__(self) -> None:
        self._app = None
        self._handler = None

    def _init_app(self) -> bool:
        """Lazy-initialize the Slack Bolt app."""
        if self._app is not None:
            return True

        bot_token = os.getenv("SLACK_BOT_TOKEN")
        app_token = os.getenv("SLACK_APP_TOKEN")

        if not bot_token or not app_token:
            logger.warning(
                "Slack tokens missing! Please set SLACK_BOT_TOKEN and SLACK_APP_TOKEN in .env"
            )
            print(
                "\n[!] WARNING: Slack tokens missing in .env!\n"
                "    Please set SLACK_BOT_TOKEN and SLACK_APP_TOKEN in your .env file to activate Slack Socket Mode.\n"
            )
            return False

        try:
            from slack_bolt import App
            from slack_bolt.adapter.socket_mode import SocketModeHandler

            self._app = App(
                token=bot_token,
                signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
            )
            self._register_commands()
            self._handler = SocketModeHandler(self._app, app_token)
            logger.info("Slack Bolt app initialized successfully")
            return True
        except Exception as exc:
            logger.error("Failed to initialize Slack app: %s", exc)
            print(f"\n[!] Slack initialization error: {exc}")
            return False

    def _register_commands(self) -> None:
        """Register Slack command handlers."""
        if self._app is None:
            return

        @self._app.command("/hermes-scan")
        def handle_scan(ack, respond, command):
            ack()
            respond("🔍 Starting internship scan...")
            bus.publish(SCAN_REQUEST, {"source": "slack", "user": command.get("user_id")})

        @self._app.command("/hermes-status")
        def handle_status(ack, respond, command):
            ack()
            bus.publish(STATUS_REQUEST, {"source": "slack"})
            respond("📊 Status check requested")

        @self._app.command("/hermes-analytics")
        def handle_analytics(ack, respond, command):
            ack()
            bus.publish(ANALYTICS_REQUEST, {"source": "slack"})
            respond("📈 Generating analytics report...")

        @self._app.message("hermes")
        def handle_mention(message, say):
            say("👋 I'm Hermes, your AI Operating System. Use `/hermes-scan` to discover internships!")

        logger.info("Slack commands registered")

    def start(self) -> None:
        """Start the Slack bot."""
        if not self._init_app():
            return
        if self._handler:
            logger.info("Starting Slack bot listener...")
            print("[+] Slack bot listener active! Waiting for slash commands...")
            self._handler.start()

    def stop(self) -> None:
        """Stop the Slack bot."""
        if self._handler:
            self._handler.close()
            logger.info("Slack bot stopped")
