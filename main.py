from fastapi import FastAPI

from classes.job import Job
from classes.application import Application

app = FastAPI()

# List all job postings
@app.get("/jobs")
async def read_jobs(status: str = None, limit: int = 10):
    return {}

# List a single job posting (by job_id)
@app.get("/jobs/{job_id}")
async def read_job(job_id: int):
    return {
        "job_id": job_id
    }

# Create a job posting
@app.post("/jobs/create")
async def create_job(job: Job):
    return job

# Close a job posting
@app.post("/jobs/close")
async def close_job(job_id: int):
    return {}

# List all applications
@app.get("/applications")
async def read_applications():
    return {}

# List all applications for a given job
@app.get("/applications/{job_id}")
async def read_job_applications(job_id: int):
    return {}

# List all applications by a given candidate (name)
@app.get("/applications/{candidate_name}")
async def read_job_applications(candidate_name: str):
    return {}

# Create an application
@app.post("/applications/create")
async def create_application(application: Application):
    return application