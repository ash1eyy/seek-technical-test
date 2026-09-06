from datetime import date
from pydantic import BaseModel

class Application(BaseModel):
    id: int
    title: str
    candidate_name: str
    candidate_email: str
    submitted_at: date