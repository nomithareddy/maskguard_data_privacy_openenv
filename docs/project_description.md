# Project Description

## Problem

Privacy and data-readiness issues are common in real-world datasets. Teams often need to detect exposed personally identifiable information, resolve data quality problems, validate schema assumptions, and flag bias risks before a dataset can be safely used downstream.

## Solution

MaskGuard Data Privacy OpenEnv packages those challenges into an OpenEnv-compatible environment. Agents receive a structured observation describing dataset issues and can respond with targeted remediation actions such as masking emails or phone numbers, removing duplicates, filling missing values, validating schema, applying policy rules, dropping risky columns, and flagging bias.

## Why It Matters

This environment is useful as a lightweight benchmark for agentic data governance. Instead of only testing one-step classification, it evaluates whether an agent can make a sequence of corrective decisions that improves both privacy posture and dataset readiness.

## What Is Included

- FastAPI OpenEnv server
- OpenEnv manifest in `openenv.yaml`
- Action and observation models
- Easy, medium, and hard task scenarios
- Local inference runner with evaluator-style logs
- Baseline policy for demonstration
- Local grading utilities

## Demo Flow

1. Run `python3 pre_validation.py` to confirm the environment responds correctly.
2. Run `python3 inference.py` to see evaluator-style episode output.
3. Run `python3 baseline/run_baseline.py` to show the environment across multiple difficulty levels.
4. Launch the FastAPI app with `python3 -m server.app --port 8000` for local serving.

## Technical Notes

The environment server uses `server.app:app` as its entrypoint. The repo also includes Docker support so the environment can be built and run in a containerized path that mirrors submission and deployment expectations.
