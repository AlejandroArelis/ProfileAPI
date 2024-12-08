from pydantic import BaseModel
from typing import List
from Profile.profile.skill_group.skill.models import Profile_skill_group_skill_out


class Profile_skill_group_in(BaseModel):
    profile_id: str
    skill_group_id: str


class Profile_skill_group_out(BaseModel):
    id: str
    skills: List[Profile_skill_group_skill_out] = []
    name: str = None
