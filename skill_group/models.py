from pydantic import BaseModel
from typing import List


class Skills_group_in(BaseModel):
    name: str


class Skills_group_out(Skills_group_in):
    id: str
