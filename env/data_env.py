from __future__ import annotations

import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"
if str(MODELS_DIR) not in sys.path:
    sys.path.insert(0, str(MODELS_DIR))

from schema import Action, Observation, Reward
from graders.grade_easy import grade_easy
from graders.grade_hard import grade_hard
from graders.grade_medium import grade_medium
from tasks import easy_tasks, hard_tasks, medium_tasks


class DataEnv:
    """Simple dataset remediation environment."""

    def __init__(self, difficulty: str = "easy", seed: int | None = None):
        self.difficulty = difficulty
        self.rng = random.Random(seed)
        self.scenario: Dict[str, Any] | None = None
        self.observation: Observation | None = None
        self.episode_steps = 0

    def _load_scenarios(self) -> List[Dict[str, Any]]:
        if self.difficulty == "easy":
            return easy_tasks.SCENARIOS
        if self.difficulty == "medium":
            return medium_tasks.SCENARIOS
        return hard_tasks.SCENARIOS

    def reset(self) -> Observation:
        scenarios = self._load_scenarios()
        self.scenario = self.rng.choice(scenarios).copy()
        self.observation = Observation(**self.scenario)
        self.episode_steps = 0
        return self.observation

    def state(self) -> Observation:
        assert self.observation is not None, "Environment not reset"
        return self.observation

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        assert self.observation is not None, "Environment not reset"
        self.episode_steps += 1
        obs = self.observation
        reward = 0.0
        info: Dict[str, Any] = {}

        if action.action_type == "DETECT_PII":
            if obs.pii_detected:
                reward += 0.2
                info["detected"] = obs.pii_detected
            else:
                reward -= 0.05

        elif action.action_type == "MASK_EMAIL":
            if "email" in obs.pii_detected:
                obs.pii_detected = [pii for pii in obs.pii_detected if pii != "email"]
                obs.policy_rules.append("mask_email")
                reward += 0.3
            else:
                reward -= 0.1

        elif action.action_type == "MASK_PHONE":
            if "phone" in obs.pii_detected:
                obs.pii_detected = [pii for pii in obs.pii_detected if pii != "phone"]
                obs.policy_rules.append("mask_phone")
                reward += 0.3
            else:
                reward -= 0.1

        elif action.action_type == "REMOVE_DUPLICATES":
            if obs.duplicates:
                obs.duplicates = False
                reward += 0.3
            else:
                reward -= 0.05

        elif action.action_type == "FILL_MISSING_VALUES":
            if obs.missing_values:
                obs.missing_values = []
                reward += 0.25
            else:
                reward -= 0.05

        elif action.action_type == "VALIDATE_SCHEMA":
            if not obs.schema_valid:
                obs.schema_valid = True
                reward += 0.4
            else:
                reward -= 0.02

        elif action.action_type == "STANDARDIZE_FORMAT":
            if obs.missing_values or obs.duplicates:
                reward += 0.1
            else:
                reward -= 0.02

        elif action.action_type == "DROP_COLUMN":
            column = (action.payload or {}).get("column")
            if column and column in obs.columns:
                obs.columns = [existing for existing in obs.columns if existing != column]
                if column == "email" and "email" in obs.pii_detected:
                    obs.pii_detected = [pii for pii in obs.pii_detected if pii != "email"]
                    reward += 0.25
                else:
                    reward -= 0.05
            else:
                reward -= 0.1

        elif action.action_type == "FLAG_BIAS":
            if obs.bias_detected:
                reward += 0.2
                obs.policy_rules.append("flag_bias")
            else:
                reward -= 0.05

        elif action.action_type == "APPLY_POLICY_RULE":
            rule = (action.payload or {}).get("rule")
            if rule:
                if rule not in obs.policy_rules:
                    obs.policy_rules.append(rule)
                    reward += 0.15
                else:
                    reward -= 0.02
            else:
                reward -= 0.05

        if not obs.schema_valid:
            reward -= 0.1

        reward = Reward(value=max(-1.0, min(1.0, reward))).value
        obs.reward = reward

        if self.difficulty == "easy":
            readiness = grade_easy(obs)
        elif self.difficulty == "medium":
            readiness = grade_medium(obs)
        else:
            readiness = grade_hard(obs)

        done = readiness >= 0.999 or self.episode_steps >= 20
        obs.done = done

        info["readiness"] = float(readiness)
        info["steps"] = self.episode_steps
        return obs, float(reward), bool(done), info
