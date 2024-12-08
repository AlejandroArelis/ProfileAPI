from bson import ObjectId

from Player.repositories import files
from Player.repositories import directories
from Player.services import tags
from Player.services import people

async def save(name:str, path: str):

    exists = await directories.get_by_path(path)

    if exists:

        exists["id"] = str(exists["_id"])
        del exists["_id"]

        return exists
    else:
        directory = {
            "type": "directory",
            "name": name,
            "path": path,
            "opened_folder": False,
            "directory_id": "root"
        }

        return await files.save(directory)


async def get_by_id(id: str, skip: int = 0, limit = 0):

    directory = await directories.get_by_id(id, skip, limit)

    directory["id"] = str(directory["_id"])
    del directory["_id"]

    if directory.get("directory_id") and directory["directory_id"] is not None:
        directory["directory_id"] = str(directory["directory_id"])

    for file in directory["files"]:
        file["id"] = str(file["_id"])
        del file["_id"]
        file["directory_id"] = str(file["directory_id"])

        # agregar cover a la carpeta
        if file["type"] != "directory" and not directory.get("image"):
            directory["image"] = file["url"]

        if file.get("code"):
            file["tags"] = await tags.get_by_id_list(file["tags"])
            file["people"] = await people.get_by_id_list(file["people"])

    return directory