# Job API

A small job marketplace API built with FastAPI. It manages jobs and applications. Storage is in-memory, so no database is required.

## How to Run

Requirements:

- [uv](https://docs.astral.sh/uv/)
- Python 3.13+

```sh
git clone <repo-url>
cd seek-technical-test
uv run fastapi dev main.py
```

uv reads `pyproject.toml` and `uv.lock`, creates a virtual environment, and installs the pinned dependencies. On the first run it does this automatically.

The server runs at `http://127.0.0.1:8000`. Interactive API docs are at `http://127.0.0.1:8000/docs`.

## Design Overview

- `main.py` defines the FastAPI app and routes. Handlers are thin. They call the store and map results to responses.
- `classes/` defines the Pydantic models. `JobCreate` and `ApplicationCreate` are the request payloads. Timestamps are generated on the server side.
- `store.py` defines the `Store` class. It keeps jobs and applications in Python lists. It owns the business rules:
  - a closed job cannot be closed again
  - an application cannot be created for a job that does not exist
  - an application cannot be created for a closed job

On startup, the lifespan seeds three sample jobs. Two are open and one is closed. This way the list endpoints return data right away.

Status codes follow a simple convention:

- missing resource: 404
- invalid action: 400
- successful create: 201

## Assumptions

- uv already installed.
- No authentication or authorisation is required.
- No frontend.
- Data is not persistent. It is held in memory and lost when the server stops.
- Job and application IDs auto-increment.
- Status and candidate name filters are case-insensitive.
- A candidate may apply to multiple jobs but cannot apply to the same job more than once.
- Pagination is applied to the list endpoints after filtering.

## Areas For Improvement

- Add real persistence with a database such as SQLite or Postgres.
- Add proper pagination instead of just a limit.
- Prevent duplicate applications for the same candidate and job.
- Add structured logging and consistent error responses.
- Add a `tests/` directory with pytest and TestClient coverage.
- Add authentication, for example to restrict who can close a job.
- Move settings such as the default limit and the seed toggle into environment variables.