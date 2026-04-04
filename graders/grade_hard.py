from __future__ import annotations

import sys
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"
if str(MODELS_DIR) not in sys.path:
    sys.path.insert(0, str(MODELS_DIR))

from schema import Observation


def grade_hard(obs: Observation) -> float:
    """Hard grader: full dataset readiness compliance."""
    score = 0.0
    parts = 4

    if not obs.pii_detected:
        score += 1.0

    if not obs.missing_values:
        score += 1.0

    if not obs.duplicates and obs.schema_valid:
        score += 1.0

    if not obs.bias_detected or ("flag_bias" in obs.policy_rules):
        score += 1.0

    return max(0.0, min(1.0, score / parts))
