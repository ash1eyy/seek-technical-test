from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query

from classes.job import JobCreate
from classes.application import ApplicationCreate
from store import Store

store = Store()


@asynccontextmanager
async def lifespan(app: FastAPI):
    store.add_job(
        title="Senior Python Developer",
        description="Build and maintain backend services.",
        location="Melbourne",
    )
    store.add_job(
        title="Junior Frontend Engineer",
        description="Work on our web application with React.",
        location="Sydney",
    )
    closed_job = store.add_job(
        title="DevOps Engineer",
        description="Managed CI/CD pipelines and cloud infrastructure.",
        location="Remote",
    )
    store.close_job(closed_job["id"])

    yield


app = FastAPI(lifespan=lifespan)


# List all job postings, optionally filtered by status
@app.get("/jobs")
async def read_jobs(
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    return store.list_jobs(status=status, page=page, page_size=page_size)


# Get details for a single job posting
@app.get("/jobs/{job_id}")
async def read_job(job_id: int):
    job = store.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


# Create a new job posting
@app.post("/jobs/create", status_code=201)
async def create_job(job: JobCreate):
    return store.add_job(
        title=job.title,
        description=job.description,
        location=job.location,
    )


# Close a job posting
@app.post("/jobs/{job_id}/close")
async def close_job(job_id: int):
    try:
        job = store.close_job(job_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


# List all applications, optionally filtered by job or candidate
@app.get("/applications")
async def read_applications(
    job_id: int | None = Query(None),
    candidate_name: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    return store.list_applications(
        job_id=job_id,
        candidate_name=candidate_name,
        page=page,
        page_size=page_size,
    )


# Submit an application for a given job
@app.post("/applications/create", status_code=201)
async def create_application(application: ApplicationCreate):
    try:
        new_application = store.add_application(
            job_id=application.job_id,
            candidate_name=application.candidate_name,
            candidate_email=application.candidate_email,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if not new_application:
        raise HTTPException(status_code=404, detail="Job not found")

    return new_application