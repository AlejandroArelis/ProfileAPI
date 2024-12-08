from bson import ObjectId
from Player.db.mongo import db

file_errors = db["file_errors"]

async def save(file_name: str, file_path:str, error):
    try:
        print(f"Guardando error para el archivo: {file_path}")
        response = await file_errors.insert_one({"file_name": file_name, "file_path": file_path, "error_message": error})
        print("respuesta")
        print(response)
        print("terminando respuesta")
    except Exception as db_error:
        print(f"Error al guardar en la base de datos: {db_error}")
        return None