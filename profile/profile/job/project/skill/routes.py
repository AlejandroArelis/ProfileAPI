from bson import ObjectId
from fastapi import APIRouter, HTTPException
from Profile.db.mongo import db
from Profile.profile.job.project.skill.models import Skill

router = APIRouter(
    prefix="/project_skill",
    tags=["project_skill"]
)

skills = db["skills"]
project_skills = db["project_skills"]


@router.get("/{project_id}")
async def get_by_project(project_id: str):
    project_skills_list = await project_skills.find({"project_id": project_id}).to_list(None)
    
    for project_skill in project_skills_list:
        skill = await skills.find_one({"_id": ObjectId(project_skill["skill_id"])})
        project_skill["id"] = str(project_skill["_id"])      
        project_skill["name"] = skill["name"]
        project_skill["image"] = skill["image"]
        
        del project_skill["_id"]
        del project_skill["skill_id"]
        del project_skill["project_id"]


    return sorted(project_skills_list, key=lambda skill: skill['name'])

@router.get("/avalible/{project_id}")
async def get_by_project(project_id: str):
    project_skills_list = await project_skills.find({"project_id": project_id}).to_list(None)
    
    unavailable_skills = [ ObjectId(project_skill["skill_id"]) for project_skill in project_skills_list]
    
    avalible_skills = await skills.find({"_id": {"$nin": unavailable_skills}}).to_list(None)
        
    for skill in avalible_skills:
        skill["id"] = str(skill["_id"])
        del skill["_id"]
        del skill["skill_group_id"]
        del skill["color"]

    return sorted(avalible_skills, key=lambda skill: skill['name'])


@router.post("/")
async def new(item: Skill):
    try:
        item_found = await project_skills.find_one({"skill_id": item.skill_id, "project_id": item.project_id})
        if item_found:
            raise HTTPException(status_code=400, detail=f"Ya se encuentra agregado")
        else:
            item_dump = item.model_dump()
            response = await project_skills.insert_one(item_dump)
            
            skill = await skills.find_one({"_id": ObjectId(item.skill_id)})
            skill["id"] = str(response.inserted_id)
            del skill["_id"]
            del skill["skill_group_id"]
            del skill["color"]
            return skill
    except Exception as e:
        raise e


@router.delete("/{item_id}")
async def delete(item_id: str):
    try:
        # Eliminación de la skill en la colección skills
        response = await project_skills.delete_one({"_id": ObjectId(item_id)})
        if response:
            return True
        else:
            raise HTTPException(status_code=404, detail="El elemento no se ha encontrado")
    except Exception as e:
        raise e