from __future__ import annotations

import sys
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"
if str(MODELS_DIR) not in sys.path:
    sys.path.insert(0, str(MODELS_DIR))

from schema import Observation


def grade_medium(obs: Observation) -> float:
    """Medium grader: email removed, duplicates removed, and missing values fixed."""
    total = 3.0
    score = 0.0

    if "email" not in obs.pii_detected:
        score += 1.0

    if not obs.duplicates:
        score += 1.0

    if not obs.missing_values:
        score += 1.0

    return max(0.0, min(1.0, score / total))
