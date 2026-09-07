from fastapi import APIRouter, Depends, HTTPException, Query

from dependencies import get_store
from models.job import JobCreate
from store import Store

router = APIRouter()


@router.get("/jobs")
async def read_jobs(
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    store: Store = Depends(get_store),
):
    return store.list_jobs(status=status, page=page, page_size=page_size)


@router.get("/jobs/{job_id}")
async def read_job(
    job_id: int,
    store: Store = Depends(get_store),
):
    job = store.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.post("/jobs/create", status_code=201)
async def create_job(
    job: JobCreate,
    store: Store = Depends(get_store),
):
    return store.add_job(
        title=job.title,
        description=job.description,
        location=job.location,
    )


@router.post("/jobs/{job_id}/open")
async def open_job(
    job_id: int,
    store: Store = Depends(get_store),
):
    try:
        job = store.open_job(job_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.post("/jobs/{job_id}/close")
async def close_job(
    job_id: int,
    store: Store = Depends(get_store),
):
    try:
        job = store.close_job(job_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
