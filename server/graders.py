from __future__ import annotations

from typing import Dict, Any


def grade_easy(state: Dict[str, Any]) -> float:
    """Easy grader: score based on whether email was removed.

    Returns 1.0 if 'email' not in pii_detected, else 0.0
    """
    pii = state.get("pii_detected", []) or []
    return 1.0 if "email" not in pii else 0.0


def grade_medium(state: Dict[str, Any]) -> float:
    """Medium grader: email removed + duplicates removed + missing values fixed.

    Each component counts as 1; normalize to [0,1].
    """
    total = 3.0
    score = 0.0

    pii = state.get("pii_detected", []) or []
    if "email" not in pii:
        score += 1.0

    if not state.get("duplicates", False):
        score += 1.0

    if not (state.get("missing_values") or []):
        score += 1.0

    return max(0.0, min(1.0, score / total))


def grade_hard(state: Dict[str, Any]) -> float:
    """Hard grader: email removed, duplicates removed, missing fixed, schema valid, bias removed.

    Five components normalized to [0,1].
    """
    total = 5.0
    score = 0.0

    pii = state.get("pii_detected", []) or []
    if "email" not in pii:
        score += 1.0

    if not state.get("duplicates", False):
        score += 1.0

    if not (state.get("missing_values") or []):
        score += 1.0

    if state.get("schema_valid", False):
        score += 1.0

    # bias_removed: either no bias_detected or bias_detected was addressed (absence)
    if not state.get("bias_detected", False):
        score += 1.0

    return max(0.0, min(1.0, score / total))
