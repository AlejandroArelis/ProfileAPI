from bson import ObjectId
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

async def get_by_id(item_id: str):
    item = await db["skills_groups"].find_one({"_id": ObjectId(item_id)})
    if item:
        return Skills_group_out(**item, id=str(item["_id"]))
    else:
        raise HTTPException(status_code=500, detail="El elemento no se ha encontrado")


@router.post("/")
async def new(item: Skills_group_in):
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
    
@router.put("/{item_id}")
async def update(item_id: str, item: Skills_group_in):
    item_dump = item.model_dump()

    result = await db["skills_groups"].update_one({"_id": ObjectId(item_id)}, {"$set": item_dump})

    if result.modified_count == 1 or result.raw_result.get('updatedExisting'):
        return await get_by_id(item_id)
    else:
        raise HTTPException(status_code=404, detail="El elemento no se ha encontrado")
    
@router.delete("/{item_id}")
async def delete(item_id: str):
    result = await db["skills_groups"].delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 1:
        return {"message": f"El elemento se ha eliminado"}
    else:
        raise HTTPException(status_code=404, detail="El elemento no se ha encontrado")