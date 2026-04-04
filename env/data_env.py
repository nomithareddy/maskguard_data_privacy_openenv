from __future__ import annotations

from typing import Tuple, Dict, Any, List
import random

from models.schema import Observation, Action, Reward
from tasks import easy_tasks, medium_tasks, hard_tasks
from graders.grade_easy import grade_easy
from graders.grade_medium import grade_medium
from graders.grade_hard import grade_hard


class DataEnv:
    """Simple dataset remediation environment.

    Methods:
        reset() -> Observation
        state() -> Observation
        step(action: Action) -> (Observation, reward, done, info)
    """

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

        # action handling
        a = action.action_type
        if a == "DETECT_PII":
            # reward for discovering PII: positive if PII exists
            if obs.pii_detected:
                reward += 0.2
                info["detected"] = obs.pii_detected
            else:
                reward -= 0.05

        elif a == "MASK_EMAIL":
            # remove email from pii_detected if present
            if "email" in obs.pii_detected:
                obs.pii_detected = [p for p in obs.pii_detected if p != "email"]
                obs.policy_rules.append("mask_email")
                reward += 0.3
            else:
                reward -= 0.1

        elif a == "MASK_PHONE":
            if "phone" in obs.pii_detected:
                obs.pii_detected = [p for p in obs.pii_detected if p != "phone"]
                obs.policy_rules.append("mask_phone")
                reward += 0.3
            else:
                reward -= 0.1

        elif a == "REMOVE_DUPLICATES":
            if obs.duplicates:
                obs.duplicates = False
                reward += 0.3
            else:
                reward -= 0.05

        elif a == "FILL_MISSING_VALUES":
            if obs.missing_values:
                obs.missing_values = []
                reward += 0.25
            else:
                reward -= 0.05

        elif a == "VALIDATE_SCHEMA":
            # if schema was invalid, fixing it grants reward; if already valid, small penalty
            if not obs.schema_valid:
                obs.schema_valid = True
                reward += 0.4
            else:
                reward -= 0.02

        elif a == "STANDARDIZE_FORMAT":
            # smoothing action - small positive if issues present
            if obs.missing_values or obs.duplicates:
                reward += 0.1
            else:
                reward -= 0.02

        elif a == "DROP_COLUMN":
            col = (action.payload or {}).get("column")
            if col and col in obs.columns:
                obs.columns = [c for c in obs.columns if c != col]
                # if dropped a PII column, consider it a fix
                if col == "email" and "email" in obs.pii_detected:
                    obs.pii_detected = [p for p in obs.pii_detected if p != "email"]
                    reward += 0.25
                else:
                    reward -= 0.05
            else:
                reward -= 0.1

        elif a == "FLAG_BIAS":
            # flagging bias is good when bias exists
            if obs.bias_detected:
                reward += 0.2
                obs.policy_rules.append("flag_bias")
            else:
                reward -= 0.05

        elif a == "APPLY_POLICY_RULE":
            rule = (action.payload or {}).get("rule")
            if rule:
                if rule not in obs.policy_rules:
                    obs.policy_rules.append(rule)
                    reward += 0.15
                else:
                    reward -= 0.02
            else:
                reward -= 0.05

        # reward shaping: negative if we made schema invalid
        if not obs.schema_valid:
            reward -= 0.1

        # clamp reward
        reward = max(-1.0, min(1.0, reward))
        obs.reward = reward

        # compute readiness via grader corresponding to difficulty
        if self.difficulty == "easy":
            readiness = grade_easy(obs)
        elif self.difficulty == "medium":
            readiness = grade_medium(obs)
        else:
            readiness = grade_hard(obs)

        # consider episode done if readiness is 1.0 or after 20 steps
        done = readiness >= 0.999 or self.episode_steps >= 20
        obs.done = done

        info["readiness"] = float(readiness)
        info["steps"] = self.episode_steps

        return obs, float(reward), bool(done), info
