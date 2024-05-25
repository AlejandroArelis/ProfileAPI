from pydantic import BaseModel
from typing import List, Optional

class Profile(BaseModel):
  name: str
  email: str
  azure_id: str
  job: Optional[str] = None
  phone: Optional[str] = None
  city: Optional[str] = None

class ProfileDB(Profile):
  id: str