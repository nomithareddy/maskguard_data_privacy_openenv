"""Inference script for OpenEnv evaluator format.

Runs the required action sequence against the local environment and prints
three evaluator-formatted lines: [START], [STEP] (per step), and [END].
"""

from typing import List, Optional

from server.maskguard_data_privacy_openenv_environment import MaskguardDataPrivacyOpenenvEnvironment
from models import MaskguardDataPrivacyOpenenvAction
from server import graders


def log_start() -> None:
    print("[START]", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    err = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={err}", flush=True)


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


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
    step = 0

    for a in actions:
        step += 1
        try:
            action = MaskguardDataPrivacyOpenenvAction(action_type=a)
            obs = env.step(action)
            reward = float(getattr(obs, "reward", 0.0) or 0.0)
            done = bool(getattr(obs, "done", False))
            rewards.append(reward)
            log_step(step=step, action=a, reward=reward, done=done, error=None)
            if done:
                break
        except Exception as exc:
            log_step(step=step, action=a, reward=0.0, done=False, error=str(exc))

    state = {
        "pii_detected": getattr(obs, "pii_detected", []),
        "duplicates": getattr(obs, "duplicates", False),
        "missing_values": getattr(obs, "missing_values", []),
        "schema_valid": getattr(obs, "schema_valid", False),
        "bias_detected": getattr(obs, "bias_detected", False),
    }

    score = float(graders.grade_hard(state))
    success = score >= 0.5

    log_end(success=success, steps=step, score=score, rewards=rewards)


if __name__ == "__main__":
    try:
        run_episode()
    except Exception:
        print("[END] success=false steps=0 score=0.000 rewards=", flush=True)
        raise
"""Inference script for OpenEnv evaluator format.

Runs the required action sequence against the local environment and prints
three evaluator-formatted lines: [START], [STEP] (per step), and [END].
"""

from typing import List, Optional

from server.maskguard_data_privacy_openenv_environment import MaskguardDataPrivacyOpenenvEnvironment
from models import MaskguardDataPrivacyOpenenvAction
from server import graders


def log_start() -> None:
    print("[START]", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    err = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={err}", flush=True)


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


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
    step = 0

    for a in actions:
        step += 1
        try:
            action = MaskguardDataPrivacyOpenenvAction(action_type=a)
            obs = env.step(action)
            reward = float(getattr(obs, "reward", 0.0) or 0.0)
            done = bool(getattr(obs, "done", False))
            rewards.append(reward)
            log_step(step=step, action=a, reward=reward, done=done, error=None)
            if done:
                break
        except Exception as exc:
            log_step(step=step, action=a, reward=0.0, done=False, error=str(exc))

    state = {
        "pii_detected": getattr(obs, "pii_detected", []),
        "duplicates": getattr(obs, "duplicates", False),
        "missing_values": getattr(obs, "missing_values", []),
        "schema_valid": getattr(obs, "schema_valid", False),
        "bias_detected": getattr(obs, "bias_detected", False),
    }

    score = float(graders.grade_hard(state))
    success = score >= 0.5

    log_end(success=success, steps=step, score=score, rewards=rewards)


if __name__ == "__main__":
    try:
        run_episode()
    except Exception:
        print("[END] success=false steps=0 score=0.000 rewards=", flush=True)
        raise
"""Inference script for OpenEnv evaluator format.

Runs the required action sequence against the local environment and prints
three evaluator-formatted lines: [START], [STEP] (per step), and [END].
"""

from typing import List, Optional

from server.maskguard_data_privacy_openenv_environment import MaskguardDataPrivacyOpenenvEnvironment
from models import MaskguardDataPrivacyOpenenvAction
from server import graders


def log_start() -> None:
    print("[START]", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    err = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={err}", flush=True)


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


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
    step = 0

    for a in actions:
        step += 1
        try:
            action = MaskguardDataPrivacyOpenenvAction(action_type=a)
            obs = env.step(action)
            reward = float(getattr(obs, "reward", 0.0) or 0.0)
            done = bool(getattr(obs, "done", False))
            rewards.append(reward)
            log_step(step=step, action=a, reward=reward, done=done, error=None)
            if done:
                break
        except Exception as exc:
            log_step(step=step, action=a, reward=0.0, done=False, error=str(exc))

    state = {
        "pii_detected": getattr(obs, "pii_detected", []),
        "duplicates": getattr(obs, "duplicates", False),
        "missing_values": getattr(obs, "missing_values", []),
        "schema_valid": getattr(obs, "schema_valid", False),
        "bias_detected": getattr(obs, "bias_detected", False),
    }

    score = float(graders.grade_hard(state))
    success = score >= 0.5

    log_end(success=success, steps=step, score=score, rewards=rewards)


if __name__ == "__main__":
    try:
        run_episode()
    except Exception:
        print("[END] success=false steps=0 score=0.000 rewards=", flush=True)
        raise
"""
Inference Script Example
===================================
MANDATORY
- Before submitting, ensure the following variables are defined in your environment configuration:
    API_BASE_URL   The API endpoint for the LLM.
    MODEL_NAME     The model identifier to use for inference.
    HF_TOKEN       Your Hugging Face / API key.
    LOCAL_IMAGE_NAME The name of the local image to use for the environment if you are using from_docker_image()
                     method

- Defaults are set only for API_BASE_URL and MODEL_NAME 
    (and should reflect your active inference setup):
    API_BASE_URL = os.getenv("API_BASE_URL", "<your-active-endpoint>")
    MODEL_NAME = os.getenv("MODEL_NAME", "<your-active-model>")
    
- The inference script must be named `inference.py` and placed in the root directory of the project
- Participants must use OpenAI Client for all LLM calls using above variables

STDOUT FORMAT
- The script must emit exactly three line types to stdout, in this order:

    [START] task=<task_name> env=<benchmark> model=<model_name>
    [STEP]  step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
    [END]   success=<true|false> steps=<n> score=<score> rewards=<r1,r2,...,rn>

  Rules:
    - One [START] line at episode begin.
    - One [STEP] line per step, immediately after env.step() returns.
    - One [END] line after env.close(), always emitted (even on exception).
    - reward and rewards are formatted to 2 decimal places.
    - done and success are lowercase booleans: true or false.
    - error is the raw last_action_error string, or null if none.
    - All fields on a single line with no newlines within a line.
    - Each tasks should return score in [0, 1]

  Example:
    [START] task=click-test env=miniwob model=Qwen3-VL-30B
    [STEP] step=1 action=click('123') reward=0.00 done=false error=null
    [STEP] step=2 action=fill('456','text') reward=0.00 done=false error=null
    [STEP] step=3 action=click('789') reward=1.00 done=true error=null
    [END] success=true steps=3 score=1.00 rewards=0.00,0.00,1.00
"""

import asyncio
import os
import textwrap
from typing import List, Optional

from openai import OpenAI

from my_env_v4 import MyEnvV4Action, MyEnvV4Env
IMAGE_NAME = os.getenv("IMAGE_NAME") # If you are using docker image 
API_KEY = os.getenv("HF_TOKEN") or os.getenv("<REDACTED_TOKEN>")

API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
TASK_NAME = os.getenv("MY_ENV_V4_TASK", "echo")
BENCHMARK = os.getenv("MY_ENV_V4_BENCHMARK", "my_env_v4")
MAX_STEPS = 8
TEMPERATURE = 0.7
MAX_TOKENS = 150
SUCCESS_SCORE_THRESHOLD = 0.1  # normalized score in [0, 1]

# Max possible reward: each token contributes 0.1, across all steps
_MAX_REWARD_PER_STEP = MAX_TOKENS * 0.1
"""Simple inference script that runs directly against the local environment.

This script follows the OpenEnv evaluator stdout format and executes a fixed
sequence of actions to demonstrate environment behavior.

It emits the three required line types (one [START], multiple [STEP], one [END]).
"""

from typing import List, Optional
import sys

from server.maskguard_data_privacy_openenv_environment import (
    MaskguardDataPrivacyOpenenvEnvironment,
)
from models import MaskguardDataPrivacyOpenenvAction
from server import graders


def log_start() -> None:
    # Minimal START line (no extra fields required by the request)
    print("[START]", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    err = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={err}", flush=True)


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


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
    step = 0
    last_error: Optional[str] = None

    for a in actions:
        step += 1
        try:
            action = MaskguardDataPrivacyOpenenvAction(action_type=a)
            obs = env.step(action)
            reward = float(getattr(obs, "reward", 0.0) or 0.0)
            done = bool(getattr(obs, "done", False))
            rewards.append(reward)
            log_step(step=step, action=a, reward=reward, done=done, error=None)
            if done:
                break
        except Exception as exc:
            last_error = str(exc)
            log_step(step=step, action=a, reward=0.0, done=False, error=last_error)

    # Compute final score using hard grader if schema invalid, otherwise medium/easy
    state = {
        "pii_detected": getattr(obs, "pii_detected", []),
        "duplicates": getattr(obs, "duplicates", False),
        "missing_values": getattr(obs, "missing_values", []),
        "schema_valid": getattr(obs, "schema_valid", False),
        "bias_detected": getattr(obs, "bias_detected", False),
    }

    # decide which grader to use: prefer hard if schema was initially invalid
    score_easy = graders.grade_easy(state)
    score_medium = graders.grade_medium(state)
    score_hard = graders.grade_hard(state)

    # pick the strictest (highest demand) grader result as the final score
    score = float(score_hard)

    success = score >= 0.999 or score >= 0.5

    log_end(success=success, steps=step, score=score, rewards=rewards)


if __name__ == "__main__":
    try:
        run_episode()
    except Exception as exc:
        # ensure [END] is still printed in case of failure
        print(f"[END] success=false steps=0 score=0.000 rewards=", flush=True)
        raise