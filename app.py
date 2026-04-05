"""Top-level ASGI entrypoint for Hugging Face Spaces and simple local startup.

This module exposes a FastAPI `app` object for the Space build system which
expects an `app` symbol at the repository top-level. It simply imports the
application created in `server.app` and re-exports it.

Usage (local dev):
    python3 app.py
    # or
    python3 -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
"""

try:
    # Import the FastAPI app created in server.app
    from server.app import app as app  # type: ignore
except Exception:  # pragma: no cover - surface import errors when running
    # If the import fails, raise a helpful message for maintainers
    raise


if __name__ == "__main__":
    # Allow simple local startup with: python3 app.py
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
