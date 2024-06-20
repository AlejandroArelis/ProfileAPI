from pydantic import BaseModel, conint


class Profile_skill_group_in(BaseModel):
    profile_id: str
    skill_group_id: str


class Profile_skill_group_out(Profile_skill_group_in):
    id: str
