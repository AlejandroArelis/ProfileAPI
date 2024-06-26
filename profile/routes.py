from fastapi import APIRouter, HTTPException, Path, Query
from bson import Binary, ObjectId
from database import db
from profile.models import ProfileOut, ProfileIn
from profile.exeptions import ProfileNotFoundException
from profile.skill_group.routes import get_profile_skill_groups

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)


@router.get("/")
async def get():
    profiles = await db["profiles"].find().to_list(None)

    return [ProfileOut(**profile, id=str(profile["_id"])) for profile in profiles]


# @router.get("/{profile_id}")
async def get_by_id(profile_id: str):
    profile = await db["profiles"].find_one({"_id": ObjectId(profile_id)})
    if profile:

        profile["profile_skill_groups"] = await get_profile_skill_groups(profile["_id"])

        return ProfileOut(**profile, id=str(profile["_id"]))
    else:
        raise ProfileNotFoundException()


@router.get("/username/{user_name}")
async def get_profile_by_user_name(user_name: str = Path(..., min_length=1)):
    profile = await db["profiles"].find_one({"user_name": user_name})
    if profile:

        profile["profile_skill_groups"] = await get_profile_skill_groups(profile["_id"])

        return ProfileOut(**profile, id=str(profile["_id"]))
    else:
        raise ProfileNotFoundException()


@router.post("/")
async def get_azure_profile(profile: ProfileIn):
    try:
        azure_id = Binary.from_uuid(profile.azure_id)
        response = await db["profiles"].find_one({"azure_id": azure_id})
        if response:
            return ProfileOut(**response, id=str(response["_id"]))
        else:
            profile.user_name = f"{profile.name.replace(' ', '')}{str(profile.azure_id).replace('-', '')}"
            profile.azure_id = azure_id
            profile_dump = profile.model_dump()
            response = await db["profiles"].insert_one(profile_dump)
            profile_dump["id"] = str(response.inserted_id)
            return ProfileOut(**profile_dump)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{profile_id}")
async def update_profile(profile_id: str, profile: ProfileIn):
    profile.azure_id = Binary.from_uuid(profile.azure_id)
    profile_dump = profile.model_dump()

    result = await db["profiles"].update_one({"_id": ObjectId(profile_id)}, {"$set": profile_dump})

    if result.modified_count == 1 or result.raw_result.get('updatedExisting'):
        return await get_by_id(profile_id)
    else:
        raise HTTPException(status_code=404, detail="Profile not found")


@router.delete("/{profile_id}")
async def delete_profile(profile_id: str):
    result = await db["profiles"].delete_one({"_id": ObjectId(profile_id)})
    if result.deleted_count == 1:
        return {"message": "Profile deleted successfully"}
    else:
        raise ProfileNotFoundException()