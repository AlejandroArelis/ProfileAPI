from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import db
from profile.skill_group.models import Profile_skill_group_in, Profile_skill_group_out


router = APIRouter(
    prefix="/profile_skill_group",
    tags=["profile_skill_group"]
)

profile_skill_groups = db["profile_skill_groups"]

# @router.get("/{profile_id}")
# async def get(profile_id: str):
#     try:
#         profile = await profiles.find_one({"_id": ObjectId(profile_id)})
#
#         if profile:
#             items = await profile_skills.find().to_list(None)
#
#             return [Profile_skill_out(**item, id=str(item["_id"])) for item in items]
#         else:
#             raise HTTPException(status_code=500, detail="El perfil no se ha encontrado")
#
#     except Exception as e:
#         raise e


@router.post("/")
async def new_profile_skill_group(item: Profile_skill_group_in):
    try:
        item_found = await profile_skill_groups.find_one({"profile_id": item.profile_id, "skill_group_id": item.skill_group_id})
        if item_found:
            raise HTTPException(status_code=400, detail=f"Este grupo de habilidades del perfil ya existe")

        item_dump = item.model_dump()
        response = await profile_skill_groups.insert_one(item_dump)
        item_dump["id"] = str(response.inserted_id)
        return Profile_skill_group_out(**item_dump)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.put("/{item_id}")
# async def update(item_id: str, item: Profile_skill_in):
#     try:
#         item_found = await profile_skills.find_one({"skill_id": item.skill_id, "profile_id": item.profile_id})
#         if item_found:
#             raise HTTPException(status_code=400, detail=f"Esta habilidad ya existe")
#
#         item_dump = item.model_dump()
#         result = await profile_skills.update_one({"_id": ObjectId(item_id)}, {"$set": item_dump})
#
#         print(result)
#         if result.modified_count == 1 or result.raw_result.get('updatedExisting'):
#             return True
#         else:
#             raise HTTPException(status_code=404, detail="La habilidad no se ha modificado")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.delete("/{item_id}")
# async def delete(item_id: str):
#     result = await profile_skills.delete_one({"_id": ObjectId(item_id)})
#     if result.deleted_count == 1:
#         return {"message": f"La habilidad se ha eliminado"}
#     else:
#         raise HTTPException(status_code=404, detail="La habilidad no fue encontrada")