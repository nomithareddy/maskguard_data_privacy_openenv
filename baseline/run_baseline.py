from __future__ import annotations

from env.data_env import DataEnv
from models.schema import Action


def baseline_policy(obs):
    """Simple policy: detect PII, mask emails/phones, remove duplicates, fill missing, validate schema."""
    actions = []
    actions.append(Action(action_type="DETECT_PII"))

    # mask known PII
    for p in list(obs.pii_detected):
        if p == "email":
            actions.append(Action(action_type="MASK_EMAIL"))
        elif p == "phone":
            actions.append(Action(action_type="MASK_PHONE"))
        else:
            # fallback to applying a policy rule
            actions.append(Action(action_type="APPLY_POLICY_RULE", payload={"rule": f"mask_{p}"}))

    if obs.duplicates:
        actions.append(Action(action_type="REMOVE_DUPLICATES"))

    if obs.missing_values:
        actions.append(Action(action_type="FILL_MISSING_VALUES"))

    if not obs.schema_valid:
        actions.append(Action(action_type="VALIDATE_SCHEMA"))

    if obs.bias_detected:
        actions.append(Action(action_type="FLAG_BIAS"))

    return actions


def run(difficulty: str = "easy") -> float:
    env = DataEnv(difficulty=difficulty)
    obs = env.reset()
    print("Initial state:", obs.dict())

    steps = 0
    while True:
        actions = baseline_policy(obs)
        if not actions:
            break
        for a in actions:
            obs, reward, done, info = env.step(a)
            print(f"Action: {a.action_type} → reward {reward}")
            steps += 1
            if done:
                break
        if done:
            break

    readiness = info.get("readiness", 0.0)
    print(f"Final readiness score: {readiness:.3f} after {steps} steps")
    return float(readiness)


if __name__ == "__main__":
    # run all difficulties sequentially for demonstration
    for d in ("easy", "medium", "hard"):
        print("\n=== Running baseline for difficulty:", d, "===")
        run(d)
