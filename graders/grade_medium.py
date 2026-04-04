from __future__ import annotations

from models.schema import Observation


def grade_medium(obs: Observation) -> float:
    """Grade fixing tasks: measure how many issues have been fixed."""
    total = 0
    fixed = 0

    # PII
    if obs.pii_detected:
        total += len(obs.pii_detected)
    else:
        total += 1
        fixed += 1

    # missing values
    total += 1
    if not obs.missing_values:
        fixed += 1

    # duplicates
    total += 1
    if not obs.duplicates:
        fixed += 1

    # schema
    total += 1
    if obs.schema_valid:
        fixed += 1

    return max(0.0, min(1.0, fixed / total))
