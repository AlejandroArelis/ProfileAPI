from datetime import datetime
from pydantic import BaseModel
from typing import List


class Job(BaseModel):
    profile_id: str
    name: str
    company_name: str
    city: str
    date_start: datetime
    date_end: datetime
    # skills: List[str] = []


# class Job_out(Job_out_in):
#     id: str
