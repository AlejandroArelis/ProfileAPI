import os
from fastapi import APIRouter, HTTPException
from Player.services import directories

router = APIRouter(prefix="/directories", tags=["directories"])

@router.get("/")
async def get_by_id(directory_id: str, skip: int = 0, limit: int = 30):
    return await directories.get_by_id(directory_id, skip, limit)