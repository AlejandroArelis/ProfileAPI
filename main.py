import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from Profile.profile.routes import router as profile_routes
from Profile.profile.job.routes import router as profile_job_routes
from Profile.profile.job.project.routes import router as profile_job_project_routes
from Profile.skill_group.routes import router as skill_group_routes
from Profile.skill_group.skill.routes import router as skill_routes
from Profile.profile.skill_group.routes import router as profile_skill_group_routes
from Profile.profile.skill_group.skill.routes import router as profile_skill_group_skill_routes
from Profile.profile.job.project.skill.routes import router as project_skill_routes
from Player.api.v1.routes import files
from Player.api.v1.routes import directories
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

ia = OpenAI()

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://alejandroarelis.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_routes)
app.include_router(profile_skill_group_routes)
app.include_router(profile_skill_group_skill_routes)
app.include_router(skill_group_routes)
app.include_router(skill_routes)
app.include_router(profile_job_routes)
app.include_router(profile_job_project_routes)
app.include_router(project_skill_routes)
app.include_router(files.router)
app.include_router(directories.router)


@app.get("/")
async def hello():
    # response = ia.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": "Who won the world series in 2020?"},
    #         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    #         {"role": "user", "content": "Where was it played?"}
    #     ]
    # )
    return {'message': "hola"}


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logging.error(f"Server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)