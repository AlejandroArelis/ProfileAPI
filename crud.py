from typing import List
from fastapi import APIRouter, HTTPException, Path
from models import Profile, ProfileDB
from database import db
from bson import ObjectId
from exceptions import ProfileNotFoundException

router = APIRouter()

async def create_profile(profile: Profile):
	# Verificar si ya existe un perfil con el mismo azure_id
	existing_profile = await db["profiles"].find_one({"azure_id": profile.azure_id})
	if existing_profile:
			raise HTTPException(status_code=400, detail="Ya existe un perfil con este azure_id")
	
	# Si no existe, insertar el nuevo perfil
	profile_dump = profile.model_dump()
	result = await db["profiles"].insert_one(profile_dump)
	profile_dump["id"] = str(result.inserted_id)
	return ProfileDB(**profile_dump)

@router.get("/profile/", response_model=List[ProfileDB])
async def get_profiles():
	profiles = await db["profiles"].find().to_list(None)
	return [ProfileDB(**profile, id=str(profile["_id"])) for profile in profiles]

@router.get("/profile/{profile_id}", response_model=ProfileDB)
async def get_profile(profile_id: str = Path(...)):
	profile = await db["profiles"].find_one({"_id": ObjectId(profile_id)})
	if profile:
		return ProfileDB(**profile, id=str(profile["_id"]))
	else:
		raise ProfileNotFoundException()

@router.post("/profile/", response_model=ProfileDB)
async def get_profile(profile: Profile):
	try:
		response = await db["profiles"].find_one({"azure_id": profile.azure_id})
		if response:
			return ProfileDB(**response, id=str(response["_id"]))
		else:
			return await create_profile(profile)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

@router.put("/profile/{profile_id}", response_model=ProfileDB)
async def update_profile(profile_id: str, profile: Profile):
	profile_dump = profile.model_dump()
	result = await db["profiles"].update_one({"_id": ObjectId(profile_id)}, {"$set": profile_dump})
	if result.modified_count == 1:
		return await get_profile(profile_id)
	else:
		raise ProfileNotFoundException()

@router.delete("/profile/{profile_id}", response_model=dict)
async def delete_profile(profile_id: str):
	result = await db["profiles"].delete_one({"_id": ObjectId(profile_id)})
	if result.deleted_count == 1:
		return {"message": "Profile deleted successfully"}
	else:
		raise ProfileNotFoundException()