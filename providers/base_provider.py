"""
Hermes AI OS — Base Provider

Abstract interface that all AI providers must implement.
Ensures uniform access to different LLM APIs.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseProvider(ABC):
    """Abstract base class for AI model providers.

    All providers expose the same ``complete()`` and ``complete_json()``
    methods so agents can switch models without code changes.
    """

    def __init__(self, name: str, model: str) -> None:
        self.name = name
        self.model = model

    @abstractmethod
    def complete(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """Send a prompt to the model and return the text response."""
        ...

    @abstractmethod
    def complete_json(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> Dict[str, Any]:
        """Send a prompt and parse the response as JSON."""
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} model={self.model!r}>"
