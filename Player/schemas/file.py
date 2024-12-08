from pydantic import BaseModel
from typing import List, Optional

class FileSchema(BaseModel):
    type: str
    name: str
    path: str
    count_finished: int
    count_seen: int
    opened_folder: bool
    url: str
    files: List['FileSchema'] = []

class FileCreateSchema(BaseModel):
    type: str
    name: str
    path: str
    count_finished: int
    count_seen: int
    opened_folder: bool
    url: str
    files: List['FileSchema'] = []
