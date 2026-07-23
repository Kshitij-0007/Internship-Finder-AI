"""
Hermes AI OS — Configuration Settings

Loads environment variables from .env file (if present) and
provides centralized access to configuration settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables without overwriting existing environment or .env file
load_dotenv()

# Base Directory
BASE_DIR = Path(__file__).parent.parent

# AI Provider Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Default AI Provider & Model
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "openai")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")

# Slack Configuration
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET", "")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN", "")

# System Settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", str(BASE_DIR / "logs" / "hermes.log"))
PERSIST_MEMORY_PATH = os.getenv("PERSIST_MEMORY_PATH", str(BASE_DIR / "data" / "memory_snapshot.json"))
