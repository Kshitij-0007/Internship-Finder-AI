"""
Hermes AI OS — Gemini Provider

Wraps the Google Generative AI (Gemini) API behind the BaseProvider interface.
"""

import json
import logging
from typing import Any, Dict

from providers.base_provider import BaseProvider
from config.settings import GEMINI_API_KEY

logger = logging.getLogger("hermes.providers.gemini")


class GeminiProvider(BaseProvider):
    """Google Gemini provider."""

    def __init__(self, model: str = "gemini-2.0-flash") -> None:
        super().__init__(name="gemini", model=model)
        self._client = None

    def _get_client(self):
        """Lazy-initialize the Gemini client."""
        if self._client is None:
            try:
                import google.generativeai as genai

                genai.configure(api_key=GEMINI_API_KEY)
                self._client = genai.GenerativeModel(self.model)
            except ImportError:
                logger.error("google-generativeai package not installed")
                raise
        return self._client

    def complete(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """Send a prompt to Gemini and return the text response."""
        model = self._get_client()
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

        response = model.generate_content(
            full_prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )
        return response.text or ""

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
            logger.warning("Failed to parse Gemini response as JSON")
            return {"raw_response": text}
