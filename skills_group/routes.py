from fastapi import APIRouter, HTTPException
from database import db
from skills_group.models import Skills_group_out, Skills_group_in

router = APIRouter(
    prefix="/skills-group",
    tags=["skills-group"]
)


@router.get("/")
async def get():
    items = await db["skills_groups"].find().to_list(None)

    return [Skills_group_out(**item, id=str(item["_id"])) for item in items]


@router.post("/")
async def now(item: Skills_group_in):
    try:
        item_found = await db["skills_groups"].find_one({"name": item.name})
        if item_found:
            raise HTTPException(status_code=400, detail=f"{item.name} ya existe")
        else:
            item_dump = item.model_dump()
            response = await db["skills_groups"].insert_one(item_dump)
            item_dump["id"] = str(response.inserted_id)
            return Skills_group_out(**item_dump)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))