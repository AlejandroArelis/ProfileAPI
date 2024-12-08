from pydantic import BaseModel


class Skill(BaseModel):
    project_id: str
    skill_id: str