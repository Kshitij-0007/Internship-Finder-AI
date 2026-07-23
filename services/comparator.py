"""
Hermes AI OS — Comparator Service

Compares job listings to detect similarities and differences.
Used by the duplicate detection agent and ranking agent.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger("hermes.services.comparator")


def compare(job_a: Dict[str, Any], job_b: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two job listings and return a similarity report.

    Returns:
        Dict with keys: similarity (float 0-1), matching_fields (list),
        confidence (int 0-100).
    """
    matching_fields = []
    total_fields = 0
    matched = 0

    fields_to_compare = ["company", "role", "location", "url"]
    for field in fields_to_compare:
        val_a = (str(job_a.get(field, "")) or "").lower().strip()
        val_b = (str(job_b.get(field, "")) or "").lower().strip()
        total_fields += 1

        if val_a and val_b and val_a == val_b:
            matched += 1
            matching_fields.append(field)

    similarity = matched / total_fields if total_fields > 0 else 0.0
    confidence = int(similarity * 100)

    return {
        "similarity": round(similarity, 3),
        "matching_fields": matching_fields,
        "confidence": confidence,
    }
