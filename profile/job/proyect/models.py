from pydantic import BaseModel, conint


class Profile_skill_in(BaseModel):
    skill_id: str
    percentage: conint(gt=0, le=100)
    profile_id: str


class Profile_skill_out(Profile_skill_in):
    id: str
