from pydantic import BaseModel
from typing import Optional


class Project(BaseModel):
    name: str
    description: str
    job_id: Optional[str] = None