"""
Hermes AI OS — Logger Service

Structured logging with console and file output.
All Hermes components use the hermes.* logger hierarchy.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
) -> logging.Logger:
    """Configure the Hermes logging system.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR).
        log_file: Optional path to a log file.
        log_format: Optional custom format string.

    Returns:
        The root 'hermes' logger.
    """
    if log_format is None:
        log_format = "%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s"

    root_logger = logging.getLogger("hermes")
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Prevent duplicate handlers on repeated calls
    if root_logger.handlers:
        return root_logger

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(console)

    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(log_format))
        root_logger.addHandler(file_handler)

    return root_logger


def log(message: str, level: str = "info") -> None:
    """Quick convenience function for logging."""
    logger = logging.getLogger("hermes")
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(message)
