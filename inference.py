"""Inference script that uses an OpenAI-compatible client and evaluator logs."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from models import MaskguardDataPrivacyOpenenvAction
from server import graders
from server.maskguard_data_privacy_openenv_environment import MaskguardDataPrivacyOpenenvEnvironment

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

SYSTEM_PROMPT = """You control a dataset privacy remediation environment.
Choose exactly one next action that improves dataset readiness.
Return strict JSON with this shape:
{"action_type": "MASK_EMAIL", "payload": null}
Allowed action_type values:
- DETECT_PII
- MASK_EMAIL
- MASK_PHONE
- REMOVE_DUPLICATES
- FILL_MISSING_VALUES
- VALIDATE_SCHEMA
- STANDARDIZE_FORMAT
- DROP_COLUMN
- FLAG_BIAS
- APPLY_POLICY_RULE
Use payload only when required by DROP_COLUMN or APPLY_POLICY_RULE.
"""


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


def build_client() -> OpenAI:
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN environment variable is required")

    return OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)


def build_user_prompt(observation: Dict[str, Any]) -> str:
    return (
        "Current observation:\n"
        f"{json.dumps(observation, indent=2, sort_keys=True)}\n\n"
        "Choose the single best next remediation action. "
        "Return JSON only."
    )


def choose_action(client: OpenAI, observation: Dict[str, Any]) -> MaskguardDataPrivacyOpenenvAction:
    response = client.responses.create(
        model=MODEL_NAME,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(observation)},
        ],
    )

    raw_output = getattr(response, "output_text", "") or ""
    if not raw_output:
        raise RuntimeError("LLM returned no output")

    try:
        action_data = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"LLM returned invalid JSON: {raw_output}") from exc

    return MaskguardDataPrivacyOpenenvAction(
        action_type=action_data["action_type"],
        payload=action_data.get("payload"),
    )


def run_episode(max_steps: int = 8) -> None:
    client = build_client()
    env = MaskguardDataPrivacyOpenenvEnvironment()
    log_start()

    obs = env.reset()
    if obs is None:
        raise RuntimeError("reset() did not return an observation")

    rewards: List[float] = []

    for step in range(1, max_steps + 1):
        observation = {
            "columns": getattr(obs, "columns", []),
            "pii_detected": getattr(obs, "pii_detected", []),
            "missing_values": getattr(obs, "missing_values", []),
            "duplicates": getattr(obs, "duplicates", False),
            "schema_valid": getattr(obs, "schema_valid", False),
            "bias_detected": getattr(obs, "bias_detected", False),
            "policy_rules": getattr(obs, "policy_rules", []),
            "reward": getattr(obs, "reward", 0.0),
            "done": getattr(obs, "done", False),
        }

        try:
            action = choose_action(client, observation)
            obs = env.step(action)
            reward = float(getattr(obs, "reward", 0.0) or 0.0)
            done = bool(getattr(obs, "done", False))
            rewards.append(reward)
            log_step(step=step, action=action.action_type, reward=reward, done=done, error=None)
            if done:
                break
        except Exception as exc:
            log_step(step=step, action="ERROR", reward=0.00, done=False, error=str(exc))
            break

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
