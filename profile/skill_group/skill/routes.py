from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import db
from profile.skill_group.skill.models import Profile_skill_group_skill_in, Profile_skill_group_skill_out
from profile.skill_group.routes import new_profile_skill_group
from profile.skill_group.models import Profile_skill_group_in, Profile_skill_group_out
from skill_group.skill.models import Skill_in


router = APIRouter(
    prefix="/profile_skill_group_skill",
    tags=["profile_skill_group_skill"]
)


profiles = db["profiles"]
profile_skill_group_skills = db["profile_skill_group_skills"]
profile_skill_groups = db["profile_skill_groups"]
skills = db["skills"]


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
async def new_profile_skill_group_skill(item: Profile_skill_group_skill_in):
    try:
        # Verificar que existe el grupo de perfil (solo tienes el id del grupo)
        skill_group = await profile_skill_groups.find_one({"_id": ObjectId(item.profile_skill_group_id)})

        # Si no existe el grupo entonces se crea en el perfil
        if skill_group is None:

            # Se obtiene el id del grupo en el catalogo mediante el id de la skill
            skill = await skills.find_one({"_id": ObjectId(item.skill_id)})

            skill = Skill_in(**skill.model_dump(), id=str(skill["_id"]))

            profile_skill_group = Profile_skill_group_in(profile_id=item.profile_id, skill_group_id=skill.skill_group)

            # Inserta el nuevo Profile_skill_group en el Profile
            profile_skill_group = await new_profile_skill_group(profile_skill_group)

            profile_skill_group = Profile_skill_group_out(**profile_skill_group.model_dump(), id=str(profile_skill_group["_id"]))

            item.profile_skill_group_id = profile_skill_group.id
        else:
            # Se agrega la nueva Profile_skill_group_skill al Profile_skill_group
            profile_skill_group_skill = await profile_skill_group_skills.insert_one()

        skill_group = await profile_skill_group_skills.find_one({"profile_skill_group_id": item.profile_skill_group_id, "skill_id": item.skill_id})


        item_found = await profile_skill_group_skills.find_one({"skill_id": item.skill_id, "profile_id": item.profile_id})
        if item_found:
            raise HTTPException(status_code=400, detail=f"Esta habilidad ya existe")

        item_dump = item.model_dump()
        response = await profile_skills.insert_one(item_dump)
        item_dump["id"] = str(response.inserted_id)
        return Profile_skill_out(**item_dump)
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