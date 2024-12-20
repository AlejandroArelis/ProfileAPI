from uuid import UUID
from pydantic import BaseModel
from typing import Optional, List
from Profile.profile.skill_group.models import Profile_skill_group_out


class ProfileIn(BaseModel):
    azure_id: UUID
    name: str
    email: str
    phone: Optional[str] = None
    city: Optional[str] = None
    degree: Optional[str] = None
    school: Optional[str] = None
    user_name: Optional[str] = None
    image: Optional[str] = None
    job: Optional[str] = None


class ProfileOut(ProfileIn):
    id: str
    skill_groups: List[Profile_skill_group_out] = []
