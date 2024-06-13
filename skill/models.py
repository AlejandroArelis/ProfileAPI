from pydantic import BaseModel


class Skill_in(BaseModel):
    name: str
    skill_group: str


class Skill_out(Skill_in):
    id: str
