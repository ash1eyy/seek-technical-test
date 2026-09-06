from datetime import date
from pydantic import BaseModel

class Job(BaseModel):
    id: int
    title: str
    description: str
    location: str
    created_at: date
    status: str