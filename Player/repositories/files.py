from bson import ObjectId
from fastapi import HTTPException

from Player.db.mongo import db

files = db["files"]
directories = db["directories"]

async def save(file_data):
    result = await files.insert_one(file_data)

    if file_data["type"] != "directory":
        await files.update_one({"_id": result.inserted_id}, {"$set": {"url":f"/files/download/{str(result.inserted_id)}"}})
    return await get_by_id(result.inserted_id)


async def get_by_path(path: str):
    return await files.find_one({"path": path})


async def get_by_id(file_id: ObjectId, recordable: bool = False):
    file = await files.find_one({"_id": file_id})
    if file:
        if recordable and file["type"] != "directory":
            await files.update_one({"_id": file["_id"]}, {"$inc": {"count_seen": 1}})

        file["id"] = str(file["_id"])
        del file["_id"]

        file["directory_id"] = str(file["directory_id"])
        return file
    return None

async def delete(id: ObjectId):
    try:
        return await files.delete_one({"_id": id})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error al eliminar el archivo: {str(e)}")
