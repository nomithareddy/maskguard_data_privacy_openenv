# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Data models for the Maskguard Data Privacy Openenv environment."""

from typing import Any, Dict, List, Optional

from openenv.core.env_server.types import Action, Observation
from pydantic import Field


class MaskguardDataPrivacyOpenenvAction(Action):
    """Action representing a dataset remediation step."""

    action_type: str = Field(..., description="Type of remediation action")
    payload: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional payload for actions like DROP_COLUMN or APPLY_POLICY_RULE.",
    )


class MaskguardDataPrivacyOpenenvObservation(Observation):
    """Observation representing dataset readiness status."""

    columns: List[str] = Field(default_factory=list)
    pii_detected: List[str] = Field(default_factory=list)
    missing_values: List[str] = Field(default_factory=list)
    duplicates: bool = False
    schema_valid: bool = True
    bias_detected: bool = False
    policy_rules: List[str] = Field(default_factory=list)

    done: bool = False
    reward: float = 0.0
    metadata: Optional[Dict[str, Any]] = None
