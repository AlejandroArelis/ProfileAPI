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
skill_groups = db["skill_groups"]


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
        # Obtener el id del grupo de skills de la skill
        skill = await skills.find_one({"_id": ObjectId(item.skill_id)})

        # skill = skill.model_dump()



        # Verificar que existe un Skill_group en un Profile del Profile_skill_group de la Skill seleccionada
        try:
            ObjectId(item.profile_skill_group_id)
            profile_skill_group = await profile_skill_groups.find_one({"_id": ObjectId(item.profile_skill_group_id), "profile_id": item.profile_id, "skill_group_id": skill["skill_group_id"]})
        except Exception as e:
            profile_skill_group = None

        # Verificar que existe el grupo de perfil (solo tienes el id del grupo)
        # skill_group = await profile_skill_groups.find_one({"_id": ObjectId(item.profile_skill_group_id)})

        print(profile_skill_group)

        # Si no existe el grupo entonces se crea en el perfil
        if profile_skill_group is None or item.profile_skill_group_id == "":

            profile_skill_group = Profile_skill_group_in(profile_id=item.profile_id, skill_group_id=skill["skill_group_id"])

            # Inserta el nuevo Profile_skill_group en el Profile
            profile_skill_group = await new_profile_skill_group(profile_skill_group)

            # profile_skill_group = profile_skill_group.model_dump()

            # profile_skill_group = Profile_skill_group_out(**profile_skill_group, id=str(profile_skill_group"_id"]))

            item.profile_skill_group_id = profile_skill_group.id

        # Validar que el Profile_skill_group_skill no exista en el Profile_skill_group del perfil
        response = await profile_skill_group_skills.find_one({"profile_skill_group_id": item.profile_skill_group_id, "skill_id": item.skill_id})

        if response:
            raise HTTPException(status_code=400, detail=f"Esta habilidad ya existe en el grupo de habilidades del perfil")

        # Se agrega la nueva Profile_skill_group_skill al Profile_skill_group
        item = item.model_dump()
        response = await profile_skill_group_skills.insert_one(item)

        item["id"] = str(response.inserted_id)
        return Profile_skill_group_skill_out(**item)
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