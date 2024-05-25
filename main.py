import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from crud import router

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:8000/profile"
    "http://localhost:4200/",
    "http://127.0.0.1:4200/",
    "http://localhost:8000/",
    "http://127.0.0.1:8000/",
    "http://localhost/",
    "http://127.0.0.1/",
    "http://127.0.0.1:8000/profile/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

app.include_router(router)

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