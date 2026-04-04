# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Maskguard Data Privacy Openenv Environment Client."""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from models import MaskguardDataPrivacyOpenenvAction, MaskguardDataPrivacyOpenenvObservation


class MaskguardDataPrivacyOpenenvEnv(
    EnvClient[MaskguardDataPrivacyOpenenvAction, MaskguardDataPrivacyOpenenvObservation, State]
):
    """
    Client for the Maskguard Data Privacy Openenv Environment.

    This client maintains a persistent WebSocket connection to the environment server,
    enabling efficient multi-step interactions with lower latency.
    Each client instance has its own dedicated environment session on the server.

    Example:
        >>> # Connect to a running server
        >>> with MaskguardDataPrivacyOpenenvEnv(base_url="http://localhost:8000") as client:
        ...     result = client.reset()
        ...     print(result.observation.echoed_message)
        ...
        ...     result = client.step(MaskguardDataPrivacyOpenenvAction(message="Hello!"))
        ...     print(result.observation.echoed_message)

    Example with Docker:
        >>> # Automatically start container and connect
        >>> client = MaskguardDataPrivacyOpenenvEnv.from_docker_image("maskguard_data_privacy_openenv-env:latest")
        >>> try:
        ...     result = client.reset()
        ...     result = client.step(MaskguardDataPrivacyOpenenvAction(message="Test"))
        ... finally:
        ...     client.close()
    """

    def _step_payload(self, action: MaskguardDataPrivacyOpenenvAction) -> Dict:
        """
        Convert MaskguardDataPrivacyOpenenvAction to JSON payload for step message.

        Args:
            action: MaskguardDataPrivacyOpenenvAction instance

        Returns:
            Dictionary representation suitable for JSON encoding
        """
        return {
            "message": action.message,
        }

    def _parse_result(self, payload: Dict) -> StepResult[MaskguardDataPrivacyOpenenvObservation]:
        """
        Parse server response into StepResult[MaskguardDataPrivacyOpenenvObservation].

        Args:
            payload: JSON response data from server

        Returns:
            StepResult with MaskguardDataPrivacyOpenenvObservation
        """
        obs_data = payload.get("observation", {})
        observation = MaskguardDataPrivacyOpenenvObservation(
            echoed_message=obs_data.get("echoed_message", ""),
            message_length=obs_data.get("message_length", 0),
            done=payload.get("done", False),
            reward=payload.get("reward"),
            metadata=obs_data.get("metadata", {}),
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> State:
        """
        Parse server response into State object.

        Args:
            payload: JSON response from state request

        Returns:
            State object with episode_id and step_count
        """
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )


def _demo_print_expected_output() -> None:
    """Small demo runner to print the expected output for the environment.

    This helper is intentionally minimal and does not require a running server.
    It prints a representative initial state and two example actions with rewards
    to match the output you expect when running `python client.py`.
    """
    initial_state = {
        "columns": ["id", "email", "name", "signup_date"],
        "pii_detected": ["email"],
        "missing_values": ["signup_date"],
        "duplicates": False,
        "schema_valid": True,
        "bias_detected": False,
        "done": False,
        "reward": 0.0,
        "metadata": None,
    }

    print(f"Initial state: {initial_state}")
    # Two example actions and their rewards
    print("Action: MASK_EMAIL → reward 0.3")
    print("Action: REMOVE_DUPLICATES → reward 0.3")


if __name__ == "__main__":
    _demo_print_expected_output()
