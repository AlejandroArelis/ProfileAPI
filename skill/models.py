from pydantic import BaseModel


class SkillIn(BaseModel):
    name: str


class SkillOut(SkillIn):
    id: str
