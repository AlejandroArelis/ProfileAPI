from pydantic import BaseModel
from typing import List, Optional

class Profile(BaseModel):
  name: str
  job: str
  email: str
  phone: str
  city: str
  azure_id: Optional[str] = None

class ProfileDB(Profile):
  id: str