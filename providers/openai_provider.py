"""
Hermes AI OS — OpenAI Provider

Wraps the OpenAI API (GPT-4o, etc.) behind the BaseProvider interface.
"""

import json
import logging
from typing import Any, Dict

from providers.base_provider import BaseProvider
from config.settings import OPENAI_API_KEY

logger = logging.getLogger("hermes.providers.openai")


class OpenAIProvider(BaseProvider):
    """OpenAI GPT provider."""

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        super().__init__(name="openai", model=model)
        self._client = None

    def _get_client(self):
        """Lazy-initialize the OpenAI client."""
        if self._client is None:
            try:
                from openai import OpenAI

                self._client = OpenAI(api_key=OPENAI_API_KEY)
            except ImportError:
                logger.error("openai package not installed")
                raise
        return self._client

    def complete(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """Send a prompt to OpenAI and return the text response."""
        client = self._get_client()
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

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
            logger.warning("Failed to parse OpenAI response as JSON")
            return {"raw_response": text}
