from __future__ import annotations

from models.schema import Observation


def grade_easy(obs: Observation) -> float:
    """Grade detection tasks: readiness is higher when issues are identified/flagged.

    Returns a score between 0 and 1 where 1 means all issues are detected/acknowledged.
    """
    issues = 0
    detected = 0

    if obs.pii_detected:
        issues += len(obs.pii_detected)
        detected += len(obs.pii_detected)

    if obs.missing_values:
        issues += len(obs.missing_values)
        # in easy tasks we treat detection as presence in missing_values
        detected += len(obs.missing_values)

    if obs.duplicates:
        issues += 1
        detected += 1

    if issues == 0:
        return 1.0
    return max(0.0, min(1.0, detected / issues))
