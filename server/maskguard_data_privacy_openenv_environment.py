from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import (
        MaskguardDataPrivacyOpenenvAction,
        MaskguardDataPrivacyOpenenvObservation,
    )
except ImportError:
    from models import (
        MaskguardDataPrivacyOpenenvAction,
        MaskguardDataPrivacyOpenenvObservation,
    )


class MaskguardDataPrivacyOpenenvEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):

        self.initial_dataset = {
            "columns": ["name", "email", "age"],
            "pii_detected": ["email"],
            "missing_values": ["age"],
            "duplicates": True,
            "schema_valid": False,
            "bias_detected": False,
        }

        self.dataset = None
        self._state = State(episode_id=str(uuid4()), step_count=0)

    def reset(self):

        self.dataset = self.initial_dataset.copy()

        self._state = State(episode_id=str(uuid4()), step_count=0)

        return MaskguardDataPrivacyOpenenvObservation(
            **self.dataset,
            done=False,
            reward=0.0,
        )

    def step(self, action: MaskguardDataPrivacyOpenenvAction):

        self._state.step_count += 1

        reward = 0.0

        if action.action_type == "MASK_EMAIL":

            if "email" in self.dataset["pii_detected"]:
                self.dataset["pii_detected"].remove("email")
                reward += 0.3

        elif action.action_type == "REMOVE_DUPLICATES":

            if self.dataset["duplicates"]:
                self.dataset["duplicates"] = False
                reward += 0.3

        elif action.action_type == "FILL_MISSING_VALUES":

            if self.dataset["missing_values"]:
                self.dataset["missing_values"] = []
                reward += 0.2

        elif action.action_type == "VALIDATE_SCHEMA":

            if not self.dataset["schema_valid"]:
                self.dataset["schema_valid"] = True
                reward += 0.2

        done = (
            len(self.dataset["pii_detected"]) == 0
            and not self.dataset["duplicates"]
            and len(self.dataset["missing_values"]) == 0
            and self.dataset["schema_valid"]
        )

        return MaskguardDataPrivacyOpenenvObservation(
            **self.dataset,
            done=done,
            reward=reward,
            metadata={"step": self._state.step_count},
        )

    @property
    def state(self):

        return self._state