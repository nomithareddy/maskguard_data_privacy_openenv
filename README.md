# Maskguard Data Privacy OpenEnv

This repository implements a small OpenEnv-compatible environment for dataset
privacy and readiness remediation. The environment exposes a dataset state with
PII, missing values, duplicates, schema issues, and bias indicators, then lets
an agent take remediation actions to improve readiness.

## What is included

- OpenEnv server in `server/`
- Pydantic action and observation models in `models.py`
- Scenario tasks for `easy`, `medium`, and `hard` in `tasks/`
- Graders in `server/graders.py` and `graders/`
- A local evaluator-style runner in `inference.py`
- A simple baseline policy in `baseline/run_baseline.py`

## Observation model

`MaskguardDataPrivacyOpenenvObservation` contains:

- `columns`
- `pii_detected`
- `missing_values`
- `duplicates`
- `schema_valid`
- `bias_detected`
- `policy_rules`
- `done`
- `reward`
- `metadata`

## Action model

`MaskguardDataPrivacyOpenenvAction` supports an `action_type` and optional `payload`.
Common actions include:

- `DETECT_PII`
- `MASK_EMAIL`
- `MASK_PHONE`
- `REMOVE_DUPLICATES`
- `FILL_MISSING_VALUES`
- `VALIDATE_SCHEMA`
- `STANDARDIZE_FORMAT`
- `DROP_COLUMN`
- `FLAG_BIAS`
- `APPLY_POLICY_RULE`

## Local setup

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the pre-validation check:

```bash
python3 pre_validation.py
```

Run the evaluator-style local episode:

```bash
python3 inference.py
```

Run the baseline policy:

```bash
python3 baseline/run_baseline.py
```

## Run the server

Start the FastAPI app locally:

```bash
python3 -m server.app --port 8000
```

The OpenEnv app entrypoint declared in `openenv.yaml` is:

```text
server.app:app
```

## Docker

Build and run the environment server:

```bash
docker build -t maskguard-data-privacy-openenv .
docker run --rm -p 8000:8000 maskguard-data-privacy-openenv
```

## Submission checklist

This repo now includes the expected hackathon submission basics:

- `openenv.yaml`
- runnable FastAPI app
- action and observation schemas
- task files for multiple difficulty levels
- local inference script
- baseline runner
- setup instructions

## Notes

The environment logic used by the OpenEnv server lives in
`server/maskguard_data_privacy_openenv_environment.py`. The separate `env/`
and `graders/` modules are kept for baseline experimentation and local grading.
