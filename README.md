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
# Maskguard Data Privacy Openenv

Project Overview
----------------

This repository implements a small OpenEnv environment that simulates dataset
readiness and privacy remediation tasks. The environment presents datasets with
PII and data-quality issues (missing values, duplicates, schema problems, and
bias indicators). Actions allow masking PII, removing duplicates, filling
missing values, validating schemas, and applying policy rules. Graders compute
readiness scores in [0.0, 1.0].

Observation Space
-----------------

Observation model: `MaskguardDataPrivacyOpenenvObservation` (see `models.py`)

Fields:

- `columns`: list of column names
- `pii_detected`: list of detected PII types (e.g., `email`, `phone`)
- `missing_values`: list of columns with missing values
- `duplicates`: bool indicating duplicate rows
- `schema_valid`: whether the dataset schema is valid
- `bias_detected`: whether potential bias is present
- `done`: episode done
- `reward`: last step reward (float)

Action Space
------------

Action model: `MaskguardDataPrivacyOpenenvAction` (see `models.py`)

Supported actions (action_type):

- `DETECT_PII`
- `MASK_EMAIL`
- `MASK_PHONE`
- `REMOVE_DUPLICATES`
- `FILL_MISSING_VALUES`
- `VALIDATE_SCHEMA`
- `STANDARDIZE_FORMAT`
- `DROP_COLUMN` (payload: {"column": "colname"})
- `FLAG_BIAS`
- `APPLY_POLICY_RULE` (payload: {"rule": "rule_name"})

Reward Strategy
---------------

Rewards are shaped to encourage fixing issues and discourage damaging actions:

- Positive reward for fixing issues (masking PII, removing duplicates, filling missing values, validating schema).
- Small negative reward when an action has no effect or harms dataset quality.
- The environment returns a per-step `reward` (float). Graders compute a
    final readiness score in [0.0, 1.0].

Task Definitions
----------------

Three top-level tasks are provided in `tasks/` (simple JSON scenarios):

- `easy.json` — detection-focused scenario
- `medium.json` — fixing-focused scenario
- `hard.json` — full readiness scenario

Each JSON contains a single dataset scenario describing the initial state.

Setup Instructions
------------------

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the inference script locally:

```bash
python3 inference.py
```

Run pre-validation checks:

```bash
python3 pre_validation.py
```

Docker Usage
------------

Build and run the Docker image which executes `inference.py`:

```bash
docker build -t maskguard-env:local .
docker run --rm maskguard-env:local
```

Inference Script Usage
----------------------

The `inference.py` script runs a fixed sequence of remediation actions and
prints the OpenEnv evaluator-format lines to stdout:

- `[START]` — start of episode
- `[STEP] ...` — one line per step with `action`, `reward` (2 decimal places), `done` (lowercase true/false), and `error` (or null)
- `[END] ...` — final line with `success` (lowercase), `steps`, `score` (0.000..1.000), and `rewards` (comma-separated, 2 decimals)

Dataset Readiness Simulation
---------------------------

The environment simulates detection and remediation of:

- Personally Identifiable Information (PII) like `email`, `phone`.
- Missing values for specified columns.
- Duplicate rows flag.
- Invalid schema flag.
- Potential dataset bias.

Grader functions (`server/graders.py`) compute final readiness scores per
difficulty level. The inference and baseline scripts demonstrate typical
interactions and scoring.

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
