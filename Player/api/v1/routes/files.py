import os

from bson import ObjectId
from fastapi import APIRouter, HTTPException
from Player.services import files
from Player.services import directories

router = APIRouter(prefix="/files", tags=["files"])

@router.get("/save/")
async def get_files(name: str, path: str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Directory not found")
    if not os.path.isdir(path):
        raise HTTPException(status_code=400, detail="Path is not a directory")

    directory = await directories.save(name, path)
    files_list = await files.analyze_directory(ObjectId(directory["id"]), directory["path"])

    return files_list


@router.get("/get_by_id/{file_id}")
async def get_file_by_id(file_id: str):
    return await files.get_by_id(file_id, True)

@router.delete("/")
async def get_file_by_id(file_id: str):
    return await files.delete(file_id)


@router.get("/download/{file_id}")
async def serve_file(file_id: str):
    # Devolver el archivo como respuesta
    return await files.download_service(file_id)