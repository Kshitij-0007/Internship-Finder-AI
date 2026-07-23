"""
Hermes AI OS — Claude Provider

Wraps the Anthropic Claude API behind the BaseProvider interface.
"""

import json
import logging
from typing import Any, Dict

from providers.base_provider import BaseProvider
from config.settings import ANTHROPIC_API_KEY

logger = logging.getLogger("hermes.providers.claude")


class ClaudeProvider(BaseProvider):
    """Anthropic Claude provider."""

    def __init__(self, model: str = "claude-sonnet-4-20250514") -> None:
        super().__init__(name="claude", model=model)
        self._client = None

    def _get_client(self):
        """Lazy-initialize the Anthropic client."""
        if self._client is None:
            try:
                from anthropic import Anthropic

                self._client = Anthropic(api_key=ANTHROPIC_API_KEY)
            except ImportError:
                logger.error("anthropic package not installed")
                raise
        return self._client

    def complete(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """Send a prompt to Claude and return the text response."""
        client = self._get_client()

        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = client.messages.create(**kwargs)
        return response.content[0].text if response.content else ""

    def complete_json(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> Dict[str, Any]:
        """Send a prompt and parse the response as JSON."""
        text = self.complete(prompt, system_prompt, temperature, max_tokens)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Failed to parse Claude response as JSON")
            return {"raw_response": text}
