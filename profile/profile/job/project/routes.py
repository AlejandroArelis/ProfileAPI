from bson import ObjectId
from fastapi import APIRouter, HTTPException
from Profile.db.mongo import db
from Profile.profile.job.project.models import Project

router = APIRouter(
    prefix="/project",
    tags=["project"]
)

projects = db["projects"]


# @router.get("/{job_id}")
# async def get_by_job(job_id: str):
#     try:
#         job = await jobs.find_one({"_id": ObjectId(job_id)})
        
#         if job:
#             projects_list = await projects.find({"job_id" : job_id}).to_list(None)
            
#             for project in projects_list:
#                 project["id"] = str(project["_id"])
#                 del project["_del"]
                
#             return projects_list 
#         else:
#             raise HTTPException(status_code=404, detail=f'No se encontr� el trabajo con id {job_id}')
#     except Exception as e:
#         raise e


@router.post("/")
async def new_project(project: Project):
    try:
        project_found = await projects.find_one({
            "job_id": {"$ne" : project.job_id },
            "name": project.name
        })

        if project_found:
            raise HTTPException(status_code=400, detail=f'No se puede crear un proyecto con el mismo nombre en el mismo trabajo')
        else:
            project = project.model_dump()
            new = await projects.insert_one(project)
            project["id"] = str(new.inserted_id)
            del project["_id"]

            return project
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}")
async def update(item_id: str, project: Project):
    try:

        project_found = await projects.find_one({"_id": ObjectId(item_id)})
        
        if project_found is None:
            raise HTTPException(status_code=404, detail="El proyecto no fue encontrado")

        project_equal = await projects.find_one({
            "_id": { "$ne": ObjectId(item_id)},
            "job_id": project_found["job_id"],
            "name": project.name
        })

        print(project_equal)

        if project_equal:
            raise HTTPException(status_code=400, detail=f'No se puede actualizar el proyecto porque ya existe otro con el mismo nombre en el mismo trabajo')


        project_updated = await projects.update_one({"_id": ObjectId(item_id)}, {"$set": {"name" : project.name, "description": project.description}})
        
        if project_updated:
            return True
        else:
            raise HTTPException(status_code=400, detail=f'No se pudo actualizar el proyecto')
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{project_id}")
async def delete(project_id: str):
    response = await projects.find_one_and_delete({"_id": ObjectId(project_id)})

    if response:
        return True
    else:
        raise HTTPException(status_code=404, detail="El proyecto no se ha encontrado")