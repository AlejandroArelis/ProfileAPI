from fastapi import HTTPException

class ProfileNotFoundException(HTTPException):
  def __init__(self):
    super().__init__(status_code=404, detail="Profile not found")