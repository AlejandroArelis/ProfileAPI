from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import db
from profile.skill_group.skill.models import Profile_skill_group_skill_in, Profile_skill_group_skill_out
from profile.skill_group.routes import new_profile_skill_group
from profile.skill_group.models import Profile_skill_group_in


router = APIRouter(
    prefix="/profile_skill_group_skill",
    tags=["profile_skill_group_skill"]
)


profiles = db["profiles"]
profile_skill_group_skills = db["profile_skill_group_skills"]
profile_skill_groups = db["profile_skill_groups"]
skills = db["skills"]
skill_groups = db["skill_groups"]


@router.get("/{profile_skill_group_id}")
async def get_profile_skill_group_skill(profile_skill_group_id: str):
    try:
        profile_skill_group = await profile_skill_groups.find_one({"_id": ObjectId(profile_skill_group_id)})

        if profile_skill_group:
            items = await profile_skill_group_skills.find({"profile_skill_group_id": profile_skill_group_id}).to_list(None)

            return [Profile_skill_group_skill_out(**item, id=str(item["_id"])) for item in items]
        else:
            raise HTTPException(status_code=500, detail="El grupo de habilidades del perfil no se ha encontrado")

    except Exception as e:
        raise e


@router.post("/")
async def new_profile_skill_group_skill(item: Profile_skill_group_skill_in):
    try:
        # Obtener el id del grupo de skills de la skill
        skill = await skills.find_one({"_id": ObjectId(item.skill_id)})

        # Buscar si el skill_group_id de la skill existe en el profile_skill_group del perfil
        profile_skill_group = await profile_skill_groups.find_one({"skill_group_id": skill["skill_group_id"], "profile_id": item.profile_id})

        if profile_skill_group is None:

            # Crea una nueva instanacia de profile_skill_group
            profile_skill_group = Profile_skill_group_in(profile_id=item.profile_id, skill_group_id=skill["skill_group_id"])

            # Inserta el nuevo Profile_skill_group en el Profile
            profile_skill_group = await new_profile_skill_group(profile_skill_group)

            profile_skill_group_skill = Profile_skill_group_skill_out(**item.model_dump(), profile_skill_group_id=profile_skill_group.id)
        else:
            profile_skill_group_skill = Profile_skill_group_skill_out(**item.model_dump(), profile_skill_group_id=str(profile_skill_group["_id"]))

        # Si el profile_skill_group existe en el profile, entonces se valida que la skill no esté repetido
        response = await profile_skill_group_skills.find_one({"profile_skill_group_id": profile_skill_group_skill.profile_skill_group_id, "skill_id": profile_skill_group_skill.skill_id})

        if response:
            raise HTTPException(status_code=400, detail=f"Esta habilidad ya existe en el grupo de habilidades del perfil")

        # Se agrega la nueva Profile_skill_group_skill al Profile_skill_group
        profile_skill_group_skill = profile_skill_group_skill.model_dump()

        del profile_skill_group_skill["id"]
        response = await profile_skill_group_skills.insert_one(profile_skill_group_skill)

        profile_skill_group_skill["id"] = str(response.inserted_id)
        return Profile_skill_group_skill_out(**profile_skill_group_skill)
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