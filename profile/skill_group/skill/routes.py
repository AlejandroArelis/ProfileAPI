from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import db
from profile.skill_group.skill.models import Profile_skill_group_skill_in, Profile_skill_group_skill_out
from profile.skill_group.routes import new_profile_skill_group, get_profile_skill_group
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
        else:
            profile_skill_group["id"] = str(profile_skill_group["_id"])
            del profile_skill_group["_id"]

        # Si el profile_skill_group existe en el profile, entonces se valida que la skill no esté repetido
        response = await profile_skill_group_skills.find_one({"profile_skill_group_id": profile_skill_group["id"], "skill_id": item.skill_id})

        if response:
            raise HTTPException(status_code=400, detail=f"Esta habilidad ya existe en el grupo de habilidades del perfil")

        profile_skill_group_skill = item.model_dump()
        profile_skill_group_skill["profile_skill_group_id"] = profile_skill_group["id"]
        await profile_skill_group_skills.insert_one(profile_skill_group_skill)
        
        profile_skill_group = await get_profile_skill_group(str(profile_skill_group["id"]))
        
        profile_skill_group["id"] = str(profile_skill_group["_id"])
        del profile_skill_group["_id"]
        del profile_skill_group["profile_id"]

        return profile_skill_group
    except Exception as e:
        raise e

@router.delete("/{profile_skill_group_skill_id}")
async def delete_profile_skill_group_skill(profile_skill_group_skill_id: str):
    try:
        profile_skill_group_skill = await profile_skill_group_skills.find_one_and_delete({'_id': ObjectId(profile_skill_group_skill_id)})
        
        if profile_skill_group_skill:
            
            skill = await skills.find_one({"_id": ObjectId(profile_skill_group_skill["skill_id"])})
            skill["id"] = str(skill["_id"])
            del skill["_id"]
         
            profile_skill_group_skills_list = await profile_skill_group_skills.find({"profile_skill_group_id": profile_skill_group_skill["profile_skill_group_id"]}).to_list(None)

            if len(profile_skill_group_skills_list) == 0:
                profile_skill_group = await profile_skill_groups.find_one_and_delete({'_id': ObjectId(profile_skill_group_skill["profile_skill_group_id"])})
                
                if profile_skill_group:
                    return skill
                else:
                    raise HTTPException(status_code=404, detail=f"La habilidad se eliminó, pero no se eliminó el grupo")
        
            return skill
        else:
            raise HTTPException(status_code=404, detail=f"La habilidad no se eliminó")
            
    except Exception as e:
        raise e


@router.put("/{profile_skill_group_skill_id}")
async def delete_profile_skill_group_skill(profile_skill_group_skill_id: str, percentage: int):
    try:
        if percentage < 1 or percentage > 100:
            raise HTTPException(status_code=400, detail="El porcentaje debe estar entre 1 y 100")
        
        profile_skill_group_skill = await profile_skill_group_skills.find_one_and_update({'_id': ObjectId(profile_skill_group_skill_id)}, {"$set": {"percentage": percentage}})

        if profile_skill_group_skill:
            return True
        else:
            raise HTTPException(status_code=404, detail=f"La habilidad no se modificó")
            
    except Exception as e:
        raise e