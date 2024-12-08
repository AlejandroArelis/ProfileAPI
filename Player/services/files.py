import os
import re
import cv2
import shutil
import asyncio
from moviepy.editor import VideoFileClip
from bson import ObjectId
from fastapi import HTTPException
from fastapi.responses import FileResponse
from Player.repositories import files
from Player.repositories import tags
from Player.repositories import people
from Player.repositories import file_error
from Player.services import directories

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv"}
INVALID_DIRECTORIES = ["$RECYCLE.BIN", "found.000", "System Volume Information", "error"]

def is_image(file: str) -> bool:
    return os.path.splitext(file)[1].lower() in IMAGE_EXTENSIONS


def is_video(file: str) -> bool:
    return os.path.splitext(file)[1].lower() in VIDEO_EXTENSIONS


async def analyze_directory(directory_id: ObjectId, directory_path: str):
    files_list = []
    try:
        for root, dirs, file_names in os.walk(directory_path):

            directory = await directories.get_by_id(str(directory_id))
            files_db = [file for file in directory['files'] if file['type'] != 'directory']
            new_files = [name for name in file_names if os.path.splitext(name)[0] not in [file["name"] for file in files_db]]
            actual_files = [file for file in files_db if f"{file['name']}{file['extension']}" in file_names]
            deleted_files = [file for file in files_db if f"{file['name']}{file['extension']}" not in file_names]

            directories_db = [file for file in directory['files'] if file['type'] == 'directory']
            new_directories = [dir for dir in dirs if dir not in [file["name"] for file in directories_db]]
            actual_directories = [dir for dir in directories_db if dir["name"] in dirs]
            deleted_directories = [dir for dir in directories_db if dir['name'] not in dirs]

            # return {'files_db': files_db, "new_files": new_files, "actual_files": actual_files, "deleted_files": deleted_files}

            # Guardar los directorios nuevos
            for dir_name in new_directories:
                if dir_name not in INVALID_DIRECTORIES:
                    directory_data = {
                        "type": "directory",
                        "name": dir_name,
                        "path": f"{root}\{dir_name}",
                        "opened_folder": False,
                        "directory_id": directory_id
                    }

                    response = await files.save(directory_data)
                    response["files"] = await analyze_directory(ObjectId(response['id']), os.path.join(root, dir_name))

                    files_list.append(response)

                # for dir_name in actual_directories:
                #     print(dir_name)
                #
                # for dir_name in deleted_directories:
                #     print(dir_name)

            for file_name in new_files:
                print("------------------------------------------------------")
                print(file_name)
                if is_image(file_name):
                    file_type = "image"
                elif is_video(file_name):
                    file_type = "video"
                else:
                    print("No ex valido")
                    continue

                processed = process_filename(os.path.splitext(file_name)[0])
                print("Procesado")

                file_data = {
                    "type": file_type,
                    "name": os.path.splitext(file_name)[0],
                    "extension": os.path.splitext(file_name)[1],
                    "path": f"{root}\{file_name}",
                    "count_finished": 0,
                    "count_seen": 0,
                    "directory_id": directory_id
                }
                print("estructurado")

                analysis = await analyze_file(f"{root}\{file_name}", file_name)
                print("Analizado")

                if analysis:
                    file_data.update(analysis)
                    print("fusionado")

                    tags_list = []
                    people_list = []
                    if processed is not None:
                        if processed.get("code"):
                            print("Tiene código")
                            file_data["code"] = processed["code"]

                            # Tags
                            tags_list = []
                            for tag in processed["tags"]:
                                print("Tiene tags")
                                exists = await tags.get_by_name(tag)
                                if exists:
                                    await tags.set_counter([ObjectId(exists["id"])], 1)
                                    tags_list.append(exists)
                                else:
                                    new = await tags.save(tag)
                                    tags_list.append(new)

                            file_data["tags"] = [ObjectId(tag["id"]) for tag in tags_list]

                            # People
                            people_list = []
                            for person in processed["people"]:
                                print("Tiene personas")
                                exists = await people.get_by_name(person)
                                if exists:
                                    await people.set_counter([ObjectId(exists["id"])], 1)
                                    people_list.append(exists)
                                else:
                                    new = await people.save(person)
                                    people_list.append(new)

                            file_data["people"] = [ObjectId(person["id"]) for person in people_list]

                        if processed.get("trim"):
                            print("Tiene cortes")
                            file_data["trim"] = processed["trim"]

                    response = await files.save(file_data)

                    if response["type"] != "directory":
                        if response.get("code"):
                            response["tags"] = tags_list
                            response["people"] = people_list

                    files_list.append(response)
                else:
                    continue

            # for file_name in actual_files:
            #     print(file_name)
            #
            # for file_name in deleted_files:
            #     print(file_name)

            break  # Evitar recorrer recursivamente más de un nivel
    except Exception as e:
        print("Error analizando el directorio", e)
        raise HTTPException(status_code=500, detail=f"Error analizando el directorio: {str(e)}")
    # print(files_list)
    return files_list


async def get_by_id(file_id: str, recordable: bool = False):
    if not ObjectId.is_valid(file_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    file = await files.get_by_id(ObjectId(file_id), recordable)

    if file is None:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    return file


async def download_service(file_id: str):
    # Verificar si el ID es válido
    if not ObjectId.is_valid(file_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    file = await files.get_by_id(ObjectId(file_id))

    if file is None:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    # Obtener el path del documento
    file_path = os.path.join(file["path"])
    print(file_path)

    # Verificar si el archivo existe en el sistema de archivos
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="El archivo no existe en el sistema de archivos")

    return FileResponse(str(file_path))


def process_filename(filename):
    # Inicializar el resultado
    result = {}

    # Extraer el código dentro de los corchetes
    code_match = re.search(r'\[(.*?)]', filename)
    if code_match:
        code = code_match.group(1)
        result['code'] = code

        # Extraer las etiquetas dentro de los paréntesis
        tags_match = re.search(r'\{(.*?)}', filename)
        tags = tags_match.group(1).split(', ') if tags_match else []
        result['tags'] = tags

        # Extraer los nombres después de las etiquetas
        names_part = re.search(r'\) (.*)', filename) if tags else re.search(r'] (.*)', filename)
        names = names_part.group(1).split(', ') if names_part else []

        # Verificar y remover el "_trimN" de los nombres
        trim = None
        processed_names = []
        for name in names:
            trim_match = re.search(r'_trim(\d+)', name)
            if trim_match:
                trim = int(trim_match.group(1))
                name = re.sub(r'_trim\d+', '', name)  # Eliminar el "_trimN"
            processed_names.append(name)

        result['people'] = processed_names

        if trim:
            result['trim'] = trim

    else:
        # Procesar archivos sin código solo si tienen "_trimN"
        trim_match = re.search(r'_trim(\d+)', filename)
        if trim_match:
            result['trim'] = int(trim_match.group(1))
            filename = re.sub(r'_trim\d+', '', filename)  # Eliminar el "_trimN"
        else:
            return None  # No se procesa el archivo si no tiene código ni trim

    return result

def get_file_size(filepath):
    """Devuelve el tamaño del archivo en bytes."""
    return os.path.getsize(filepath)

async def analyze_file(filepath, file_name: str):
    """Analiza si el archivo es una imagen o video y devuelve sus propiedades."""
    file_info = {
        "width": None,
        "height": None,
        "duration": None,
        "size_bytes": get_file_size(filepath)
    }
    print("tamaño de archivo")

    # Intenta abrir el archivo como imagen
    print("Intentando abrir como imagen")
    img = cv2.imread(filepath)
    if img is not None:
        print("Imagen abierto")
        # Es una imagen
        file_info["width"], file_info["height"] = img.shape[1], img.shape[0]
        return file_info

    # Si no es imagen, intenta como video

    print("Intentando abrir como video")
    try:
        clip = VideoFileClip(filepath)
        print("Video abierto")
        file_info["width"], file_info["height"] = clip.size
        file_info["duration"] = clip.duration
        return file_info
    except Exception as e:
        print(f"Error al analizar el archivo")
        error_message = str(e)
        if "failed to read the duration" in error_message:
            error_message = "failed to read the duration"

            try:
                os.remove(filepath)
            except Exception as e:
                print("No se pudo eliminar el archivo en la ruta", filepath)
        else:
            error_message = "Otro error"
            shutil.move(filepath, os.path.join(r"H:\error", file_name))
            print(f"Archivo movido")

        # Guarda solo el mensaje filtrado
        response = await file_error.save(file_name, filepath, error_message)
        print("respuesta", response)
        return None

async def delete(id: str):
    if ObjectId.is_valid(id):
        file = await files.get_by_id(ObjectId(id))

        if file:
            if file.get("code"):
                await tags.set_counter([ObjectId(tag) for tag in file["tags"]], -1)
                await people.set_counter([ObjectId(tag) for tag in file["people"]], -1)


            response = await files.delete(ObjectId(id))
            print(response)
        else:
            raise HTTPException(status_code=500, detail=f"El archivo no existe")