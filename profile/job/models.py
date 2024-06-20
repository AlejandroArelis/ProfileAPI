from pydantic import BaseModel
from typing import List


class Job_out_in(BaseModel):
    name: str
    company_name: str
    city: str
    date_start: str
    date_end: str
    skills: List[str] = []


class Job_out(Job_out_in):
    id: str
