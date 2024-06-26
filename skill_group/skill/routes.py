from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import db
from skill_group.skill.models import Skill_in, Skill_out

router = APIRouter(
    prefix="/skill",
    tags=["skill"]
)

skills = db["skills"]
skill_groups = db["skill_groups"]


@router.get("/")
async def get_all():
    items = await skills.find().to_list(None)

    return [Skill_out(**item, id=str(item["_id"])) for item in items]


@router.get("/{skill_group}")
async def get_by_group(skill_group: str):
    items = await skills.find({"skill_group": skill_group}).to_list(None)

    return [Skill_out(**item, id=str(item["_id"])) for item in items]


# @router.get("/{item_id}")
async def get_by_id(item_id: str):
    item = await skills.find_one({"_id": ObjectId(item_id)})
    if item:
        return Skill_out(**item, id=str(item["_id"]))
    else:
        raise HTTPException(status_code=500, detail="El elemento no se ha encontrado")


@router.post("/")
async def new(item: Skill_in):
    try:
        item_found = await skills.find_one({"name": item.name, "skill_group_id": item.skill_group_id})
        if item_found:
            raise HTTPException(status_code=400, detail=f"{item.name} ya existe")
        else:
            item_dump = item.model_dump()
            response = await skills.insert_one(item_dump)
            item_dump["id"] = str(response.inserted_id)

            return Skill_out(**item_dump)
    except Exception as e:
        raise e


@router.put("/{item_id}")
async def update(item_id: str, item: Skill_in):
    try:
        item_found = await skills.find_one({"name": item.name})
        if item_found:
            raise HTTPException(status_code=400, detail=f"\"{item.name}\" ya existe")

        item_dump = item.model_dump()

        result = await skills.update_one({"_id": ObjectId(item_id)}, {"$set": item_dump})

        if result.modified_count == 1 or result.raw_result.get('updatedExisting'):
            return True
        else:
            raise HTTPException(status_code=404, detail="El elemento no se ha encontrado")
    except Exception as e:
        raise e


@router.delete("/{item_id}")
async def delete(item_id: str):
    try:
        # Busca el skill
        item = await skills.find_one({"_id": ObjectId(item_id)})

        # Si no lo encuentra lanza una excepción
        if not item:
            raise HTTPException(status_code=404, detail=f"La habilidad no fue encontrada")

        # Obtiene el documento completo del padre de la skill
        skill_group = await skill_groups.find_one({"_id": ObjectId(item["skill_group"])})
        if skill_group:
            # Remueve el id de la skill de la lista de skills y la actualiza
            skill_group["skills"].remove(item_id)
            await skill_groups.update_one({"_id": skill_group["_id"]}, {"$set": {"skills": skill_group["skills"]}})
        else:
            raise HTTPException(status_code=404, detail=f"El id del grupo de habilidad no fue encontrado")

        # Eliminación de la skill en la colección skills
        result = await skills.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 1:
            return {"message": f"El elemento se ha eliminado"}
        else:
            raise HTTPException(status_code=404, detail="El elemento no se ha encontrado")
    except Exception as e:
        raise e