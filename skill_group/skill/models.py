from pydantic import BaseModel


class Skill_in(BaseModel):
    name: str
    skill_group_id: str


class Skill_out(Skill_in):
    id: str
