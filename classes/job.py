from datetime import datetime
from pydantic import BaseModel


class Job(BaseModel):
    id: int
    title: str
    description: str
    location: str
    created_at: datetime
    status: str = "OPEN"


class JobCreate(BaseModel):
    title: str
    description: str
    location: str
