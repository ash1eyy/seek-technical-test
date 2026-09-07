from fastapi import APIRouter, Depends, HTTPException, Query

from dependencies import get_store
from models.application import ApplicationCreate
from store import Store

router = APIRouter()


@router.get("/applications")
async def read_applications(
    job_id: int | None = Query(None),
    candidate_name: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    store: Store = Depends(get_store),
):
    return store.list_applications(
        job_id=job_id,
        candidate_name=candidate_name,
        page=page,
        page_size=page_size,
    )


@router.post("/applications/create", status_code=201)
async def create_application(
    application: ApplicationCreate,
    store: Store = Depends(get_store),
):
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
