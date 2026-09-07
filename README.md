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
- Add a `tests/` directory with pytest and TestClient coverage.
- Add authentication, for example to restrict who can close a job.
- Add format validation for emails, names, phone number etc.
- Move settings such as the default limit and the seed toggle into environment variables.