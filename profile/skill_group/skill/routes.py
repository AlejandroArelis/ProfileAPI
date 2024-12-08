from bson import ObjectId
from fastapi import APIRouter, HTTPException
from Profile.db.mongo import db
from Profile.skill_group.skill.models import Skill_in, Skill_out

router = APIRouter(
    prefix="/skill",
    tags=["skill"]
)

skills = db["skills"]
skill_groups = db["skill_groups"]
profile_skill_group_skills = db["profile_skill_group_skills"]


@router.get("/")
async def get_all():
    items = await skills.find().to_list(None)

    return [Skill_out(**item, id=str(item["_id"])) for item in items]


@router.get("/{skill_group_id}")
async def get_by_group(skill_group_id: str):
    items = await skills.find({"skill_group_id": skill_group_id}).to_list(None)

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
        item_found = await skills.find_one({"name": item.name, "_id" : { "$ne" : ObjectId(item_id)}})
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

        # Eliminación de la skill en la colección skills
        result = await skills.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 1:
            return {"message": f"El elemento se ha eliminado"}
        else:
            raise HTTPException(status_code=404, detail="El elemento no se ha encontrado")
    except Exception as e:
        raise e
    
@router.get("/avalible/{profile_id}")
async def get_available(profile_id: str):
    try:
        profile_skill_group_skills_list = await profile_skill_group_skills.find({"profile_id": profile_id}).to_list(None)
        
        profile_skill_group_skills_ids = [ObjectId(profile_skill_group_skill["skill_id"]) for profile_skill_group_skill in profile_skill_group_skills_list]
            
        skills_list = await skills.find({"_id": {"$nin": profile_skill_group_skills_ids}}).to_list(None)
        
        return [{"id": str(skill["_id"]), "name": skill["name"]} for skill in skills_list]
                                          
    except Exception as e:
        raise e