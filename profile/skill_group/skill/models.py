from pydantic import BaseModel, conint


class Profile_skill_group_skill_in(BaseModel):
    percentage: conint(gt=0, le=100) # type: ignore
    skill_id: str
    profile_id: str


class Profile_skill_group_skill_out(BaseModel):
    id: str = ""
    percentage: conint(gt=0, le=100) # type: ignore
    name: str = None
    image: str = None
    color: str = None
