"""
Hermes AI OS — Agents Package

All agents inherit from BaseAgent and communicate exclusively
through events on the core event bus.
"""

from agents.base import BaseAgent

__all__ = ["BaseAgent"]
