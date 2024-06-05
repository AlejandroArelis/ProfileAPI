from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional

# class Profile:
#   id: str
#   name: str
#   email: str 
#   phone: str
#   user_name: str
#   city: str
#   degree: str
#   school: str
#   image: str
#   job: str

#   def __init__(self, id, name, email, phone, user_name, city, degree, school, image, job):
#     self.id = id
#     self.name = name
#     self.email = email
#     self.phone = phone
#     self.user_name = user_name
#     self.city = city
#     self.degree = degree
#     self.school = school
#     self.image = image
#     self.job = job

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