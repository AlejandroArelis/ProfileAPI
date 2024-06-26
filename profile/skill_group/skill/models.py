from pydantic import BaseModel, conint


class Profile_skill_group_skill_in(BaseModel):
    percentage: conint(gt=0, le=100)
    skill_id: str
    profile_id: str


class Profile_skill_group_skill_out(Profile_skill_group_skill_in):
    id: str = ""
    profile_skill_group_id: str
