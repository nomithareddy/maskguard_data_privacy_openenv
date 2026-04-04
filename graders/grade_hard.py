from __future__ import annotations

from models.schema import Observation


def grade_hard(obs: Observation) -> float:
    """Hard grader: full dataset readiness compliance.

    Score is based on absence of issues, schema validity, and presence of policy rules
    when PII existed originally.
    """
    score = 0.0
    parts = 4

    # no PII left
    if not obs.pii_detected:
        score += 1.0

    # no missing values
    if not obs.missing_values:
        score += 1.0

    # no duplicates and schema valid
    if not obs.duplicates and obs.schema_valid:
        score += 1.0

    # bias addressed or not present
    if not obs.bias_detected or ("flag_bias" in obs.policy_rules):
        score += 1.0

    return max(0.0, min(1.0, score / parts))
