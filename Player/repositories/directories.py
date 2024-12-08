from bson import ObjectId
from Player.db.mongo import db

directories = db["files"]

async def get_by_path(path: str):
    return await directories.find_one({"path": path})


async def get_by_id(directory_id: str, skip: int = 0, limit = 0):
    if skip == 0 and limit == 0:
        if directory_id == "root":
            directory = {
                "_id": "root",
                "name": "Directorios base",
                "path": "",
                "files": await directories.find({"directory_id": "root"}).to_list(None)
            }
        else:
            directory = await directories.find_one({"_id": ObjectId(directory_id)})
            directory["files"] = await directories.find({"directory_id": directory["_id"]}).to_list(None)

        return directory
    else:
        if directory_id == "root":
            directory = {
                "_id": "root",
                "name": "Directorios base",
                "path": "",
                "files": await directories.find({"directory_id": "root"}).skip(skip).limit(limit).to_list(limit)
            }
        else:
            directory = await directories.find_one({"_id": ObjectId(directory_id)})
            directory["files"] = await directories.find({"directory_id": directory["_id"]}).skip(skip).limit(
                limit).to_list(limit)

        return directory