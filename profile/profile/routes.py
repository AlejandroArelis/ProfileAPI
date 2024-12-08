import uuid
from fastapi import APIRouter, HTTPException, Path
from bson import Binary, ObjectId
from Profile.db.mongo import db
from Profile.profile.models import ProfileOut, ProfileIn
from Profile.profile.exeptions import ProfileNotFoundException
from Profile.profile.skill_group.routes import get_profile_skill_groups


from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

ia = OpenAI()

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)

profiles = db["profiles"]
jobs = db["jobs"]
projects = db["projects"]
profile_skill_groups = db["profile_skill_groups"]
profile_skill_group_skills = db["profile_skill_group_skills"]
skill_groups = db["skill_groups"]
skills = db["skills"]
project_skills = db["project_skills"]

@router.get("/")
async def get():
    profiles_list = await db["profiles"].find().to_list(None)

    return [ProfileOut(**profile, id=str(profile["_id"])) for profile in profiles_list]


# @router.get("/{profile_id}")
async def get_by_id(profile_id: str):
    profile = await profiles.find_one({"_id": ObjectId(profile_id)})
    if profile:

        profile["profile_skill_groups"] = await get_profile_skill_groups(profile["_id"])

        return ProfileOut(**profile, id=str(profile["_id"]))
    else:
        raise ProfileNotFoundException()


@router.get("/username/{user_name}")
async def get_profile_by_user_name(user_name: str = Path(..., min_length=1)):
    try:
        profile = await profiles.find_one({"user_name": user_name})
        if profile:
            profile["azure_id"] = uuid.UUID(bytes=profile['azure_id'])
            profile["id"] = str(profile["_id"])
            del profile["_id"]
            
            # skill_groups
            profile_skill_groups_list = await profile_skill_groups.find({"profile_id": profile["id"]}).to_list(None)

            for profile_skill_group in profile_skill_groups_list:
                
                del profile_skill_group["profile_id"]
                profile_skill_group["id"] = str(profile_skill_group["_id"])
                del profile_skill_group["_id"]
                
                skill_group = await skill_groups.find_one({"_id": ObjectId(profile_skill_group["skill_group_id"])})
                profile_skill_group["name"] = skill_group["name"]
                del profile_skill_group["skill_group_id"]

                # skills
                profile_skill_group_skills_list = await profile_skill_group_skills.find({"profile_skill_group_id": profile_skill_group["id"]}).to_list(None)
                
                for profile_skill_group_skill in profile_skill_group_skills_list:
                    
                    profile_skill_group_skill["id"] = str(profile_skill_group_skill["_id"])
                    del profile_skill_group_skill["_id"]
                    
                    del profile_skill_group_skill["profile_id"]
                    del profile_skill_group_skill["profile_skill_group_id"]
                    
                    skill = await skills.find_one({"_id": ObjectId(profile_skill_group_skill["skill_id"])})
                    profile_skill_group_skill["name"] = skill["name"]
                    profile_skill_group_skill["color"] = skill["color"]
                    profile_skill_group_skill["image"] = skill["image"]
                    
                    del profile_skill_group_skill["skill_id"]
                    
                profile_skill_group["skills"] = profile_skill_group_skills_list

            profile["skill_groups"] = profile_skill_groups_list

            jobs_list = await jobs.find({"profile_id": profile["id"]}).to_list(None)
        
            for job in jobs_list:
            
                job["id"] = str(job["_id"])
                del job["_id"]
            
                projects_list = await projects.find({"job_id" : job["id"]}).to_list(None)
            
                for project in projects_list:
                    project["id"] = str(project["_id"])
                    del project["_id"]
                    del project["job_id"]
                    
                    project_skills_list = await project_skills.find({"project_id": project["id"]}).to_list(None)
    
                    for project_skill in project_skills_list:
                        skill = await skills.find_one({"_id": ObjectId(project_skill["skill_id"])})
                        project_skill["id"] = str(project_skill["_id"])      
                        project_skill["name"] = skill["name"]
                        project_skill["image"] = skill["image"]
        
                        del project_skill["_id"]
                        del project_skill["skill_id"]
                        del project_skill["project_id"]


                    project["skills"] = sorted(project_skills_list, key=lambda skill: skill['name'])
            
                job["projects"] = projects_list
               
            profile["jobs"] = jobs_list

            return profile
        else:
            raise ProfileNotFoundException()
    except Exception as e:
        raise e

@router.post("/")
async def get_azure_profile(profile: ProfileIn):
    try:
        azure_id = Binary.from_uuid(profile.azure_id)
        profile = await profiles.find_one({"azure_id": azure_id})
        if profile:
            profile["azure_id"] = uuid.UUID(bytes=profile['azure_id'])
            profile["id"] = str(profile["_id"])
            del profile["_id"]
            
            # skill_groups
            profile_skill_groups_list = await profile_skill_groups.find({"profile_id": profile["id"]}).to_list(None)

            for profile_skill_group in profile_skill_groups_list:
                
                del profile_skill_group["profile_id"]
                profile_skill_group["id"] = str(profile_skill_group["_id"])
                del profile_skill_group["_id"]
                
                skill_group = await skill_groups.find_one({"_id": ObjectId(profile_skill_group["skill_group_id"])})
                profile_skill_group["name"] = skill_group["name"]
                del profile_skill_group["skill_group_id"]

                # skills
                profile_skill_group_skills_list = await profile_skill_group_skills.find({"profile_skill_group_id": profile_skill_group["id"]}).to_list(None)
                
                for profile_skill_group_skill in profile_skill_group_skills_list:
                    
                    profile_skill_group_skill["id"] = str(profile_skill_group_skill["_id"])
                    del profile_skill_group_skill["_id"]
                    
                    del profile_skill_group_skill["profile_id"]
                    del profile_skill_group_skill["profile_skill_group_id"]
                    
                    skill = await skills.find_one({"_id": ObjectId(profile_skill_group_skill["skill_id"])})
                    profile_skill_group_skill["name"] = skill["name"]
                    profile_skill_group_skill["color"] = skill["color"]
                    profile_skill_group_skill["image"] = skill["image"]
                    
                    del profile_skill_group_skill["skill_id"]
                    
                profile_skill_group["skills"] = profile_skill_group_skills_list

            profile["skill_groups"] = profile_skill_groups_list

            jobs_list = await jobs.find({"profile_id": profile["id"]}).to_list(None)
        
            for job in jobs_list:
            
                job["id"] = str(job["_id"])
                del job["_id"]
            
                projects_list = await projects.find({"job_id" : job["id"]}).to_list(None)
            
                for project in projects_list:
                    project["id"] = str(project["_id"])
                    del project["_id"]
                    del project["job_id"]
                    
                    project_skills_list = await project_skills.find({"project_id": project["id"]}).to_list(None)
    
                    for project_skill in project_skills_list:
                        skill = await skills.find_one({"_id": ObjectId(project_skill["skill_id"])})
                        project_skill["id"] = str(project_skill["_id"])      
                        project_skill["name"] = skill["name"]
                        project_skill["image"] = skill["image"]
        
                        del project_skill["_id"]
                        del project_skill["skill_id"]
                        del project_skill["project_id"]

                    project["skills"] = sorted(project_skills_list, key=lambda skill: skill['name'])
            
                job["projects"] = projects_list
               
            profile["jobs"] = jobs_list

            return profile
        else:
            profile.user_name = f"{profile.name.replace(' ', '')}{str(profile.azure_id).replace('-', '')}"
            profile.azure_id = azure_id
            profile_dump = profile.model_dump()
            response = await profiles.insert_one(profile_dump)
            profile_dump["id"] = str(response.inserted_id)
            return ProfileOut(**profile_dump)
    except Exception as e:
        raise e


@router.put("/{profile_id}")
async def update_profile(profile_id: str, profile: ProfileIn):
    profile.azure_id = Binary.from_uuid(profile.azure_id)
    profile_dump = profile.model_dump()

    result = await profiles.update_one({"_id": ObjectId(profile_id)}, {"$set": profile_dump})

    if result.modified_count == 1 or result.raw_result.get('updatedExisting'):
        return await get_by_id(profile_id)
    else:
        raise HTTPException(status_code=404, detail="Profile not found")


@router.delete("/{profile_id}")
async def delete_profile(profile_id: str):
    result = await profiles.delete_one({"_id": ObjectId(profile_id)})
    if result.deleted_count == 1:
        return {"message": "Profile deleted successfully"}
    else:
        raise ProfileNotFoundException()


@router.get("/ejemplo")
async def hello():
    response = ia.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=500,
        messages=[
            {"role": "user", "content": "Who are you"}
        ]
    )
    return {'message': response}