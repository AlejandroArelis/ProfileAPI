import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from profile.routes import router as profile_routes
from skill_group.routes import router as skill_group_routes
from skill.routes import router as skill_routes

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_routes)
app.include_router(skill_group_routes)
app.include_router(skill_routes)


@app.get("/")
def hello():
  return {'message': 'Holi'}


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logging.error(f"Server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )