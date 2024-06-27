from pydantic import BaseModel, conint


class Profile_skill_group_skill_in(BaseModel):
    percentage: conint(gt=0, le=100)
    skill_id: str
    profile_id: str


class Profile_skill_group_skill_out(BaseModel):
    id: str = ""
    # profile_skill_group_id: str
    name: str = None
    percentage: conint(gt=0, le=100)
