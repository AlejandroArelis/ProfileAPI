from bson import ObjectId
from pydantic import BaseModel, Field

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values=None):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

class FileModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    type: str
    name: str
    path: str
    count_finished: int
    count_seen: int
    opened_folder: bool
    url: str
    files: list['FileModel']

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        alias_generator = lambda x: "id" if x == "_id" else x