from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"
for path in (ROOT, MODELS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from env.data_env import DataEnv
from schema import Action


def baseline_policy(obs):
    """Simple policy that clears common readiness blockers."""
    actions = [Action(action_type="DETECT_PII")]

    for pii_type in list(obs.pii_detected):
        if pii_type == "email":
            actions.append(Action(action_type="MASK_EMAIL"))
        elif pii_type == "phone":
            actions.append(Action(action_type="MASK_PHONE"))
        elif pii_type in obs.columns:
            actions.append(Action(action_type="DROP_COLUMN", payload={"column": pii_type}))
        else:
            actions.append(Action(action_type="APPLY_POLICY_RULE", payload={"rule": f"mask_{pii_type}"}))

    if obs.duplicates:
        actions.append(Action(action_type="REMOVE_DUPLICATES"))

    if obs.missing_values:
        actions.append(Action(action_type="FILL_MISSING_VALUES"))

    if not obs.schema_valid:
        actions.append(Action(action_type="VALIDATE_SCHEMA"))

    if obs.bias_detected and "flag_bias" not in obs.policy_rules:
        actions.append(Action(action_type="FLAG_BIAS"))

    return actions


def run(difficulty: str = "easy") -> float:
    env = DataEnv(difficulty=difficulty)
    obs = env.reset()
    print("Initial state:", obs.model_dump())

    steps = 0
    info = {"readiness": 0.0}
    while True:
        actions = baseline_policy(obs)
        if not actions:
            break

        done = False
        for action in actions:
            obs, reward, done, info = env.step(action)
            print(f"Action: {action.action_type} -> reward {reward}")
            steps += 1
            if done:
                break

        if done:
            break

    readiness = info.get("readiness", 0.0)
    print(f"Final readiness score: {readiness:.3f} after {steps} steps")
    return float(readiness)


if __name__ == "__main__":
    for difficulty in ("easy", "medium", "hard"):
        print(f"\n=== Running baseline for difficulty: {difficulty} ===")
        run(difficulty)
