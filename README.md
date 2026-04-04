# Maskguard Data Privacy Openenv

This project provides a simple OpenEnv-style environment for dataset privacy
and remediation tasks. It includes Pydantic models for observations, actions,
reward shaping, a DataEnv implementation, scenario tasks at three difficulty
levels, graders, and a baseline runner.

## Observation space

Observation model: `models.schema.Observation` (Pydantic)

Fields:
- columns: list of column names
- pii_detected: list of detected PII types (e.g., `email`, `phone`)
- missing_values: list of columns with missing values
- duplicates: bool indicating duplicate rows
- schema_valid: whether the dataset schema is valid
- bias_detected: whether potential bias is present
- policy_rules: list of applied policy rule names

## Action space

Supported actions (`models.schema.Action.action_type`):

- DETECT_PII
- MASK_EMAIL
- MASK_PHONE
- REMOVE_DUPLICATES
- FILL_MISSING_VALUES
- VALIDATE_SCHEMA
- STANDARDIZE_FORMAT
- DROP_COLUMN (payload: {"column": "colname"})
- FLAG_BIAS
- APPLY_POLICY_RULE (payload: {"rule": "rule_name"})

## Reward strategy

Rewards use shaping:
- Positive reward for fixing issues (masking PII, removing duplicates, filling missing values, validating schema).
- Negative reward for actions that damage quality (dropping useful columns, acting with no effect).
- Final readiness score between 0.0 and 1.0 computed by graders per difficulty.

## Tasks

15 scenarios included across difficulties:
- 5 easy (detection-focused)
- 5 medium (fix-focused)
- 5 hard (full readiness)

Files:
- `env/data_env.py` — environment implementation
- `models/schema.py` — Pydantic models
- `tasks/` — scenario definitions
- `graders/` — graders for each difficulty
- `baseline/run_baseline.py` — example baseline runner

## Setup

Install requirements:

```bash
python3 -m pip install -r requirements.txt
```

Run baseline locally:

```bash
python3 baseline/run_baseline.py
```

## Docker

Build and run the Docker image:

```bash
docker build -t maskguard-env:local .
docker run --rm maskguard-env:local
```
---
title: Maskguard Data Privacy Openenv Environment Server
emoji: ⏲️
colorFrom: gray
colorTo: gray
sdk: docker
pinned: false
app_port: 8000
base_path: /web
tags:
  - openenv
---

# Maskguard Data Privacy Openenv Environment

A simple test environment that echoes back messages. Perfect for testing the env APIs as well as demonstrating environment usage patterns.

## Quick Start

The simplest way to use the Maskguard Data Privacy Openenv environment is through the `MaskguardDataPrivacyOpenenvEnv` class:

```python
from maskguard_data_privacy_openenv import MaskguardDataPrivacyOpenenvAction, MaskguardDataPrivacyOpenenvEnv

try:
    # Create environment from Docker image
    maskguard_data_privacy_openenvenv = MaskguardDataPrivacyOpenenvEnv.from_docker_image("maskguard_data_privacy_openenv-env:latest")

    # Reset
    result = maskguard_data_privacy_openenvenv.reset()
    print(f"Reset: {result.observation.echoed_message}")

    # Send multiple messages
    messages = ["Hello, World!", "Testing echo", "Final message"]

    for msg in messages:
        result = maskguard_data_privacy_openenvenv.step(MaskguardDataPrivacyOpenenvAction(message=msg))
        print(f"Sent: '{msg}'")
        print(f"  → Echoed: '{result.observation.echoed_message}'")
        print(f"  → Length: {result.observation.message_length}")
        print(f"  → Reward: {result.reward}")

finally:
    # Always clean up
    maskguard_data_privacy_openenvenv.close()
```

That's it! The `MaskguardDataPrivacyOpenenvEnv.from_docker_image()` method handles:
- Starting the Docker container
- Waiting for the server to be ready
- Connecting to the environment
- Container cleanup when you call `close()`

## Building the Docker Image

Before using the environment, you need to build the Docker image:

```bash
# From project root
docker build -t maskguard_data_privacy_openenv-env:latest -f server/Dockerfile .
```

## Deploying to Hugging Face Spaces

You can easily deploy your OpenEnv environment to Hugging Face Spaces using the `openenv push` command:

```bash
# From the environment directory (where openenv.yaml is located)
openenv push

# Or specify options
openenv push --namespace my-org --private
```

The `openenv push` command will:
1. Validate that the directory is an OpenEnv environment (checks for `openenv.yaml`)
2. Prepare a custom build for Hugging Face Docker space (enables web interface)
3. Upload to Hugging Face (ensuring you're logged in)

### Prerequisites

- Authenticate with Hugging Face: The command will prompt for login if not already authenticated

### Options

- `--directory`, `-d`: Directory containing the OpenEnv environment (defaults to current directory)
- `--repo-id`, `-r`: Repository ID in format 'username/repo-name' (defaults to 'username/env-name' from openenv.yaml)
- `--base-image`, `-b`: Base Docker image to use (overrides Dockerfile FROM)
- `--private`: Deploy the space as private (default: public)

### Examples

```bash
# Push to your personal namespace (defaults to username/env-name from openenv.yaml)
openenv push

# Push to a specific repository
openenv push --repo-id my-org/my-env

# Push with a custom base image
openenv push --base-image ghcr.io/meta-pytorch/openenv-base:latest

# Push as a private space
openenv push --private

# Combine options
openenv push --repo-id my-org/my-env --base-image custom-base:latest --private
```

After deployment, your space will be available at:
`https://huggingface.co/spaces/<repo-id>`

The deployed space includes:
- **Web Interface** at `/web` - Interactive UI for exploring the environment
- **API Documentation** at `/docs` - Full OpenAPI/Swagger interface
- **Health Check** at `/health` - Container health monitoring
- **WebSocket** at `/ws` - Persistent session endpoint for low-latency interactions

## Environment Details

### Action
**MaskguardDataPrivacyOpenenvAction**: Contains a single field
- `message` (str) - The message to echo back

### Observation
**MaskguardDataPrivacyOpenenvObservation**: Contains the echo response and metadata
- `echoed_message` (str) - The message echoed back
- `message_length` (int) - Length of the message
- `reward` (float) - Reward based on message length (length × 0.1)
- `done` (bool) - Always False for echo environment
- `metadata` (dict) - Additional info like step count

### Reward
The reward is calculated as: `message_length × 0.1`
- "Hi" → reward: 0.2
- "Hello, World!" → reward: 1.3
- Empty message → reward: 0.0

## Advanced Usage

### Connecting to an Existing Server

If you already have a Maskguard Data Privacy Openenv environment server running, you can connect directly:

```python
from maskguard_data_privacy_openenv import MaskguardDataPrivacyOpenenvEnv

# Connect to existing server
maskguard_data_privacy_openenvenv = MaskguardDataPrivacyOpenenvEnv(base_url="<ENV_HTTP_URL_HERE>")

# Use as normal
result = maskguard_data_privacy_openenvenv.reset()
result = maskguard_data_privacy_openenvenv.step(MaskguardDataPrivacyOpenenvAction(message="Hello!"))
```

Note: When connecting to an existing server, `maskguard_data_privacy_openenvenv.close()` will NOT stop the server.

### Using the Context Manager

The client supports context manager usage for automatic connection management:

```python
from maskguard_data_privacy_openenv import MaskguardDataPrivacyOpenenvAction, MaskguardDataPrivacyOpenenvEnv

# Connect with context manager (auto-connects and closes)
with MaskguardDataPrivacyOpenenvEnv(base_url="http://localhost:8000") as env:
    result = env.reset()
    print(f"Reset: {result.observation.echoed_message}")
    # Multiple steps with low latency
    for msg in ["Hello", "World", "!"]:
        result = env.step(MaskguardDataPrivacyOpenenvAction(message=msg))
        print(f"Echoed: {result.observation.echoed_message}")
```

The client uses WebSocket connections for:
- **Lower latency**: No HTTP connection overhead per request
- **Persistent session**: Server maintains your environment state
- **Efficient for episodes**: Better for many sequential steps

### Concurrent WebSocket Sessions

The server supports multiple concurrent WebSocket connections. To enable this,
modify `server/app.py` to use factory mode:

```python
# In server/app.py - use factory mode for concurrent sessions
app = create_app(
    MaskguardDataPrivacyOpenenvEnvironment,  # Pass class, not instance
    MaskguardDataPrivacyOpenenvAction,
    MaskguardDataPrivacyOpenenvObservation,
    max_concurrent_envs=4,  # Allow 4 concurrent sessions
)
```

Then multiple clients can connect simultaneously:

```python
from maskguard_data_privacy_openenv import MaskguardDataPrivacyOpenenvAction, MaskguardDataPrivacyOpenenvEnv
from concurrent.futures import ThreadPoolExecutor

def run_episode(client_id: int):
    with MaskguardDataPrivacyOpenenvEnv(base_url="http://localhost:8000") as env:
        result = env.reset()
        for i in range(10):
            result = env.step(MaskguardDataPrivacyOpenenvAction(message=f"Client {client_id}, step {i}"))
        return client_id, result.observation.message_length

# Run 4 episodes concurrently
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(run_episode, range(4)))
```

## Development & Testing

### Direct Environment Testing

Test the environment logic directly without starting the HTTP server:

```bash
# From the server directory
python3 server/maskguard_data_privacy_openenv_environment.py
```

This verifies that:
- Environment resets correctly
- Step executes actions properly
- State tracking works
- Rewards are calculated correctly

### Running Locally

Run the server locally for development:

```bash
uvicorn server.app:app --reload
```

## Project Structure

```
maskguard_data_privacy_openenv/
├── .dockerignore         # Docker build exclusions
├── __init__.py            # Module exports
├── README.md              # This file
├── openenv.yaml           # OpenEnv manifest
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock                # Locked dependencies (generated)
├── client.py              # MaskguardDataPrivacyOpenenvEnv client
├── models.py              # Action and Observation models
└── server/
    ├── __init__.py        # Server module exports
    ├── maskguard_data_privacy_openenv_environment.py  # Core environment logic
    ├── app.py             # FastAPI application (HTTP + WebSocket endpoints)
    └── Dockerfile         # Container image definition
```
