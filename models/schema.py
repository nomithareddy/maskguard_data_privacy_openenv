from __future__ import annotations

from typing import List, Optional, Dict, Any, Literal

from pydantic import BaseModel, Field


ActionType = Literal[
    "DETECT_PII",
    "MASK_EMAIL",
    "MASK_PHONE",
    "REMOVE_DUPLICATES",
    "FILL_MISSING_VALUES",
    "VALIDATE_SCHEMA",
    "STANDARDIZE_FORMAT",
    "DROP_COLUMN",
    "FLAG_BIAS",
    "APPLY_POLICY_RULE",
]


class Action(BaseModel):
    action_type: ActionType = Field(..., description="Type of remediation action")
    payload: Optional[Dict[str, Any]] = Field(default=None, description="Optional action payload")


class Observation(BaseModel):
    columns: List[str] = Field(default_factory=list)
    pii_detected: List[str] = Field(default_factory=list)
    missing_values: List[str] = Field(default_factory=list)
    duplicates: bool = False
    schema_valid: bool = True
    bias_detected: bool = False
    policy_rules: List[str] = Field(default_factory=list)

    # runtime fields
    done: bool = False
    reward: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


class Reward(BaseModel):
    value: float = Field(..., ge=-1.0, le=1.0)
