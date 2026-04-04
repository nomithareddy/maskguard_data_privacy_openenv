# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""FastAPI application for the Maskguard Data Privacy Openenv environment."""

try:
    from openenv.core.env_server.http_server import create_app
except Exception as e:  # pragma: no cover
    raise ImportError(
        "openenv is required for the web interface. Install dependencies with '\n    pip install -r requirements.txt\n'"
    ) from e

try:
    from ..models import MaskguardDataPrivacyOpenenvAction, MaskguardDataPrivacyOpenenvObservation
    from .maskguard_data_privacy_openenv_environment import MaskguardDataPrivacyOpenenvEnvironment
except (ImportError, ValueError):
    from models import MaskguardDataPrivacyOpenenvAction, MaskguardDataPrivacyOpenenvObservation
    from server.maskguard_data_privacy_openenv_environment import MaskguardDataPrivacyOpenenvEnvironment


app = create_app(
    MaskguardDataPrivacyOpenenvEnvironment,
    MaskguardDataPrivacyOpenenvAction,
    MaskguardDataPrivacyOpenenvObservation,
    env_name="maskguard_data_privacy_openenv",
    max_concurrent_envs=1,
)


def main(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Run the environment server locally."""
    import uvicorn

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    main(port=args.port)
