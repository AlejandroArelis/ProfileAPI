from fastapi import APIRouter
from database import db
from skill.models import SkillOut


router = APIRouter(
    prefix="/skill",
    tags=["skill"]
)


@router.get("/")
async def get():
    items = await db["skills-group"].find().to_list(None)

    return [SkillOut(**item, id=str(item["_id"])) for item in items]
