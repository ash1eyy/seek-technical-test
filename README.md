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

## Project Structure

```
├── main.py                  # App setup, lifespan, router registration
├── dependencies.py          # Dependency injection (provides the store to routers)
├── store.py                 # In-memory data store and business logic
├── models/
│   ├── job.py               # Pydantic model for creating jobs
│   └── application.py       # Pydantic model for creating applications
├── routers/
│   ├── jobs.py              # Job-related endpoints
│   └── applications.py      # Application-related endpoints
└── tests/
    ├── conftest.py          # Shared fixtures (store, TestClient)
    ├── test_store.py        # Unit tests for Store business logic
    └── test_api.py          # Integration tests for endpoints
```

## Design Overview

- `main.py` creates the FastAPI app, handles startup via the lifespan function, and registers the routers. It's kept pretty minimal.
- `routers/jobs.py` has all the job endpoints (list, get, create, open, close).
- `routers/applications.py` has the application endpoints (list, create).
- `dependencies.py` provides a `get_store` function so the routers can access the store without importing it directly. The store lives on `app.state` after startup.
- `models/` defines the Pydantic models. `JobCreate` and `ApplicationCreate` are the request payloads. Timestamps are generated server-side.
- `store.py` defines the `Store` class. Jobs and applications are stored in plain Python lists. It handles the business rules:
  - a closed job cannot be closed again
  - an application cannot be created for a job that does not exist
  - an application cannot be created for a closed job

On startup the lifespan seeds three sample jobs. Two are open, one is closed. That way the list endpoints return data immediately.

Status codes follow a simple convention:

- missing resource: 404
- invalid action: 400
- successful create: 201

## Example Requests

The server needs to be running for these to work. Each command is a `curl` that either reads data (GET) or sends new data (POST). Two variants are shown: Linux Bash and Windows CMD. GET commands are the same in both, so they're only listed once.

### List all jobs (optionally filter by status)

```sh
curl http://127.0.0.1:8000/jobs
curl "http://127.0.0.1:8000/jobs?status=OPEN"
curl "http://127.0.0.1:8000/jobs?page=1&page_size=10"
```

### Get one job

```sh
curl http://127.0.0.1:8000/jobs/1
```

### Create a job

Linux Bash:

```sh
curl -X POST http://127.0.0.1:8000/jobs/create \
  -H "Content-Type: application/json" \
  -d '{"title": "Backend Engineer", "description": "Build backend services.", "location": "Melbourne"}'
```

Windows CMD:

```cmd
curl -X POST http://127.0.0.1:8000/jobs/create -H "Content-Type: application/json" -d "{\"title\": \"Backend Engineer\", \"description\": \"Build backend services.\", \"location\": \"Melbourne\"}"
```

### Close a job

```sh
curl -X POST http://127.0.0.1:8000/jobs/1/close
```

### List applications (optionally filter by job or candidate)

```sh
curl http://127.0.0.1:8000/applications
curl "http://127.0.0.1:8000/applications?job_id=1"
curl "http://127.0.0.1:8000/applications?candidate_name=Alice"
```

### Submit an application

Linux Bash:

```sh
curl -X POST http://127.0.0.1:8000/applications/create \
  -H "Content-Type: application/json" \
  -d '{"job_id": 1, "candidate_name": "Alice", "candidate_email": "alice@example.com"}'
```

Windows CMD:

```cmd
curl -X POST http://127.0.0.1:8000/applications/create -H "Content-Type: application/json" -d "{\"job_id\": 1, \"candidate_name\": \"Alice\", \"candidate_email\": \"alice@example.com\"}"
```

## Running Tests

First, sync the dev dependencies:

Linux Bash:

```sh
uv sync --extra dev
```

Windows CMD:

```cmd
uv sync --extra dev
```

Run all tests:

Linux Bash:

```sh
uv run pytest tests/ -v
```

Windows CMD:

```cmd
uv run pytest tests/ -v
```

Run only the unit tests (Store logic, no HTTP):

```sh
uv run pytest tests/test_store.py -v
```

Run only the API integration tests:

```sh
uv run pytest tests/test_api.py -v
```

Tests use a fresh in-memory store per test, so they don't depend on the seed data from the lifespan. You do not need the server running to execute them.

## Assumptions

- Python & uv already installed.
- No authentication or authorisation is required.
- No frontend.
- Data is not persistent. It is held in memory and lost when the server stops.
- Job and application IDs auto-increment.
- Status and candidate name filters are case-insensitive.
- A candidate may apply to multiple jobs but cannot apply to the same job more than once.
- Pagination is applied to the list endpoints after filtering.

## Areas For Improvement

- Add real persistence with a database such as SQLite or Postgres.
- Add structured logging and consistent error responses.
- Add authentication, for example to restrict who can close a job.
- Use unique identifiers for IDs instead of plain integers.
- Add format validation for emails, names, job status, etc.
- Move settings such as the default limit and the seed toggle into environment variables.