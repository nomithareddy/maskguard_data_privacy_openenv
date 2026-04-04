"""Inference script that prints evaluator-formatted episode logs."""

from typing import List, Optional

from models import MaskguardDataPrivacyOpenenvAction
from server import graders
from server.maskguard_data_privacy_openenv_environment import MaskguardDataPrivacyOpenenvEnvironment


def log_start() -> None:
    print("[START]", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    err = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} "
        f"done={str(done).lower()} error={err}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{reward:.2f}" for reward in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} "
        f"score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


def run_episode() -> None:
    env = MaskguardDataPrivacyOpenenvEnvironment()
    log_start()

    obs = env.reset()
    if obs is None:
        raise RuntimeError("reset() did not return an observation")

    actions = [
        "MASK_EMAIL",
        "REMOVE_DUPLICATES",
        "FILL_MISSING_VALUES",
        "VALIDATE_SCHEMA",
    ]

    rewards: List[float] = []

    for step, action_name in enumerate(actions, start=1):
        try:
            action = MaskguardDataPrivacyOpenenvAction(action_type=action_name)
            obs = env.step(action)
            reward = float(getattr(obs, "reward", 0.0) or 0.0)
            done = bool(getattr(obs, "done", False))
            rewards.append(reward)
            log_step(step=step, action=action_name, reward=reward, done=done, error=None)
            if done:
                break
        except Exception as exc:
            log_step(step=step, action=action_name, reward=0.0, done=False, error=str(exc))

    state = {
        "pii_detected": getattr(obs, "pii_detected", []),
        "duplicates": getattr(obs, "duplicates", False),
        "missing_values": getattr(obs, "missing_values", []),
        "schema_valid": getattr(obs, "schema_valid", False),
        "bias_detected": getattr(obs, "bias_detected", False),
    }
    score = float(graders.grade_hard(state))
    success = score >= 0.5
    log_end(success=success, steps=len(rewards), score=score, rewards=rewards)


if __name__ == "__main__":
    try:
        run_episode()
    except Exception:
        print("[END] success=false steps=0 score=0.000 rewards=", flush=True)
        raise
