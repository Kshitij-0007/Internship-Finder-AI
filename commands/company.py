"""
Hermes AI OS — Company Command

Look up information about a specific company.
"""

import logging
from typing import Any, Dict, Optional

from memory.shared_memory import memory

logger = logging.getLogger("hermes.commands.company")


def company(name: str) -> Optional[Dict[str, Any]]:
    """Look up a company's internship listings from shared memory.

    Args:
        name: Company name to search for.

    Returns:
        Dict of company data, or None if not found.
    """
    logger.info("Company lookup: %s", name)

    # Search through stored jobs
    all_data = memory.get_all()
    results = []

    for key, value in all_data.items():
        if isinstance(value, dict) and name.lower() in key.lower():
            results.append(value)

    if results:
        logger.info("Found %d listing(s) for '%s'", len(results), name)
        return {"company": name, "listings": results}

    logger.info("No listings found for '%s'", name)
    return None
