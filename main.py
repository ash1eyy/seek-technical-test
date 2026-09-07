from contextlib import asynccontextmanager

from fastapi import FastAPI

from routers.applications import router as applications_router
from routers.jobs import router as jobs_router
from store import Store


@asynccontextmanager
async def lifespan(app: FastAPI):
    store = Store()
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
    app.state.store = store

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(jobs_router)
app.include_router(applications_router)
