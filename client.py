# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Client for the Maskguard Data Privacy Openenv environment."""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from models import MaskguardDataPrivacyOpenenvAction, MaskguardDataPrivacyOpenenvObservation


class MaskguardDataPrivacyOpenenvEnv(
    EnvClient[MaskguardDataPrivacyOpenenvAction, MaskguardDataPrivacyOpenenvObservation, State]
):
    """Persistent client for interacting with the environment server."""

    def _step_payload(self, action: MaskguardDataPrivacyOpenenvAction) -> Dict:
        return action.model_dump(exclude_none=True)

    def _parse_result(self, payload: Dict) -> StepResult[MaskguardDataPrivacyOpenenvObservation]:
        obs_data = payload.get("observation", {})
        observation = MaskguardDataPrivacyOpenenvObservation(**obs_data)

        return StepResult(
            observation=observation,
            reward=payload.get("reward", observation.reward),
            done=payload.get("done", observation.done),
        )

    def _parse_state(self, payload: Dict) -> State:
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )


if __name__ == "__main__":
    print(
        "Use this client by connecting to a running server, for example: "
        "MaskguardDataPrivacyOpenenvEnv(base_url='http://localhost:8000')"
    )
