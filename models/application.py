from datetime import datetime
from pydantic import BaseModel


class Application(BaseModel):
    id: int
    job_id: int
    candidate_name: str
    candidate_email: str
    submitted_at: datetime


class ApplicationCreate(BaseModel):
    job_id: int
    candidate_name: str
    candidate_email: str
