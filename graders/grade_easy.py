from __future__ import annotations

import sys
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"
if str(MODELS_DIR) not in sys.path:
    sys.path.insert(0, str(MODELS_DIR))

from schema import Observation


def grade_easy(obs: Observation) -> float:
    """Easy grader: score based on whether email was removed."""
    return 1.0 if "email" not in obs.pii_detected else 0.0
