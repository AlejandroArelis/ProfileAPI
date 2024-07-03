from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import db
from profile.job.models import Job
from datetime import datetime

router = APIRouter(
    prefix="/job",
    tags=["job"]
)

jobs = db["jobs"]
profiles = db["profiles"]
proyects = db["proyects"]


# @router.get("/")
# async def get():
#     items = await jobs.find().to_list(None)

#     return [Skills_group_out(**item, id=str(item["_id"])) for item in items]


@router.get("/{item_id}")
async def get_by_profile(profile_id: str):
    try:
        jobs_list = await jobs.find({"profile_id": profile_id}).to_list(None)
        
        for job in jobs_list:
            
            job["id"] = str(job["_id"])
            del job["_id"]
        
        return jobs_list
    except Exception as e:
        raise e


@router.post("/")
async def new_job(job: Job):
    try:
        job_found = await jobs.find_one({
            "name": job.name,
            "company_name": job.company_name,
            "profile_id": job.profile_id,
            "$or": [
                {
                    "$and": [
                        {"date_start": {"$lt": job.date_end}},
                        {"date_end": {"$gt": job.date_start}}
                    ]
                },
                {
                    "$and": [
                        {"date_start": {"$gte": job.date_start, "$lt": job.date_end}},
                        {"date_end": {"$gte": job.date_end}}
                    ]
                },
                {
                    "$and": [
                        {"date_start": {"$lte": job.date_start}},
                        {"date_end": {"$gt": job.date_start, "$lte": job.date_end}}
                    ]
                }
            ]
        })

        if job_found:
            raise HTTPException(status_code=400, detail=f'No se puede crear un empleo de {job.name} en {job.company_name} con fechas empalmadas')
        else:
            job = job.model_dump()
            response = await jobs.insert_one(job)
            job["id"] = str(response.inserted_id)
            del job["_id"]

            return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}")
async def update(job_id: str, job: Job):
    try:

        job_found = await jobs.find_one({"_id": ObjectId(job_id)})
        if job_found is None:
            raise HTTPException(status_code=404, detail="Job no encontrado")

        job_found = await jobs.find_one({
            "_id": {"$ne": ObjectId(job_id)},  # Excluir el job que se está actualizando
            "name": job.name,
            "company_name": job.company_name,
            "profile_id": job.profile_id,
            "$or": [
                {
                    "$and": [
                        {"date_start": {"$lt": job.date_end}},
                        {"date_end": {"$gt": job.date_start}}
                    ]
                },
                {
                    "$and": [
                        {"date_start": {"$gte": job.date_start, "$lt": job.date_end}},
                        {"date_end": {"$gte": job.date_end}}
                    ]
                },
                {
                    "$and": [
                        {"date_start": {"$lte": job.date_start}},
                        {"date_end": {"$gt": job.date_start, "$lte": job.date_end}}
                    ]
                }
            ]
        })

        if job_found:
            raise HTTPException(status_code=400, detail=f'No se puede actualizar el trabajo con fechas empalmadas con otro trabajo en la misma empresa y mismo puesto')

        job_updated = await jobs.update_one({"_id": ObjectId(job_id)}, {"$set": job.model_dump()})
        
        if job_updated:
            return True
        else:
            raise HTTPException(status_code=400, detail=f'No se pudo actualizar el trabajo')
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{job_id}")
async def delete(job_id: str):
    response = await jobs.find_one_and_delete({"_id": ObjectId(job_id)})

    if response:
        return {"message": f"El elemento se ha eliminado"}
    else:
        raise HTTPException(status_code=404, detail="El elemento no se ha encontrado")