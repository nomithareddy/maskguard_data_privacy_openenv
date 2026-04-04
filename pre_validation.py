"""Pre-validation script that exercises the environment API.

This script imports `MaskguardDataPrivacyOpenenvEnvironment`, calls reset(), then
performs a single step with action_type="MASK_EMAIL". It verifies that the
observation and reward fields are present, prints success/failure, and raises
an exception if validation fails.
"""

from __future__ import annotations

from server.maskguard_data_privacy_openenv_environment import MaskguardDataPrivacyOpenenvEnvironment
from models import MaskguardDataPrivacyOpenenvAction


def main() -> None:
    env = MaskguardDataPrivacyOpenenvEnvironment()

    obs = env.reset()
    if obs is None:
        print("FAIL: reset() returned no observation")
        raise RuntimeError("reset() returned no observation")

    # perform a mask email step
    action = MaskguardDataPrivacyOpenenvAction(action_type="MASK_EMAIL")
    obs2 = env.step(action)

    # verify observation exists and has reward
    reward = getattr(obs2, "reward", None)
    if obs2 is None or reward is None:
        print("FAIL: step did not return observation or reward")
        raise RuntimeError("step did not return observation or reward")

    print("SUCCESS: pre_validation checks passed")


if __name__ == "__main__":
    main()