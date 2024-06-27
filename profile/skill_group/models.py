from pydantic import BaseModel, conint
from typing import List
from profile.skill_group.skill.models import Profile_skill_group_skill_out
from skill_group.models import Skills_group_out


class Profile_skill_group_in(BaseModel):
    profile_id: str
    skill_group_id: str


class Profile_skill_group_out(BaseModel):
    id: str
    skills: List[Profile_skill_group_skill_out] = []
    name: str = None
