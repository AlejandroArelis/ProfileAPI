from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import db
from skill_group.models import Skills_group_out, Skills_group_in
from skill.routes import get as get_skills
import json
router = APIRouter(
    prefix="/skill-group",
    tags=["skill-group"]
)


@router.get("/")
async def get():
    items = await db["skill_groups"].find().to_list(None)

    return [Skills_group_out(**item, id=str(item["_id"])) for item in items]


@router.get("/{item_id}")
async def get_by_id(item_id: str):
    try:
        item = await db["skill_groups"].find_one({"_id": ObjectId(item_id)})
        if item:
            # skills = await get_skills(item_id)
            return Skills_group_out(**item, id=str(item["_id"]))
        else:
            raise HTTPException(status_code=500, detail="El elemento no se ha encontrado")
    except Exception as e:
        raise e


@router.post("/")
async def new(item: Skills_group_in):
    try:
        item_found = await db["skill_groups"].find_one({"name": item.name})
        if item_found:
            raise HTTPException(status_code=400, detail=f"\"{item.name}\" ya existe")
        else:
            item_dump = item.model_dump()
            response = await db["skill_groups"].insert_one(item_dump)
            item_dump["id"] = str(response.inserted_id)
            return Skills_group_out(**item_dump)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}")
async def update(item_id: str, item: Skills_group_in):
    try:
        item_found = await db["skill_groups"].find_one({"name": item.name})
        if item_found:
            raise HTTPException(status_code=400, detail=f"\"{item.name}\" ya existe")

        item_dump = item.model_dump()

        result = await db["skill_groups"].update_one({"_id": ObjectId(item_id)}, {"$set": item_dump})

        if result.modified_count == 1 or result.raw_result.get('updatedExisting'):
            return await get_by_id(item_id)
        else:
            raise HTTPException(status_code=404, detail="El elemento no se ha encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}")
async def delete(item_id: str):
    result = await db["skill_groups"].delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 1:
        return {"message": f"El elemento se ha eliminado"}
    else:
        raise HTTPException(status_code=404, detail="El elemento no se ha encontrado")