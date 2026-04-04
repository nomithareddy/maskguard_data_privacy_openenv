# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Data models for the Maskguard Data Privacy Openenv Environment.

The maskguard_data_privacy_openenv environment is a simple test environment that echoes back messages.
"""

from openenv.core.env_server.types import Action, Observation
from pydantic import Field
from typing import List, Optional, Dict




class MaskguardDataPrivacyOpenenvAction(Action):
    """Action representing a dataset remediation step."""

    action_type: str = Field(
        ...,
        description="Type of remediation action (MASK_EMAIL, REMOVE_DUPLICATES, FILL_MISSING_VALUES, VALIDATE_SCHEMA)",
    )


class MaskguardDataPrivacyOpenenvObservation(Observation):
    """
    Observation representing dataset readiness status.
    """

    columns: List[str] = Field(default_factory=list)
    pii_detected: List[str] = Field(default_factory=list)
    missing_values: List[str] = Field(default_factory=list)
    duplicates: bool = False
    schema_valid: bool = True
    bias_detected: bool = False

    done: bool = False
    reward: float = 0.0
    metadata: Optional[Dict] = None
