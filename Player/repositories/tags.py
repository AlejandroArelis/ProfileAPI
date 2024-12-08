from bson import ObjectId
from typing import List
from Player.db.mongo import db

tags = db["tags"]

async def save(name):
    new = await tags.insert_one({"name": name, "counter": 1})
    return await get_by_id(new.inserted_id)

async def get_by_id(id: ObjectId):
    tag = await tags.find_one({"_id": id})

    if tag:
        tag["id"] = str(tag["_id"])
        del tag["_id"]

    return tag

async def get_by_name(name):
    tag = await tags.find_one({"name": name})

    if tag:
        tag["id"] = str(tag["_id"])
        del tag["_id"]

    return tag

async def get_by_id_list(id_list: List[ObjectId]):
    return await tags.find({"_id": {"$in": id_list}}).to_list(None)


async def set_counter(id_list: List[ObjectId], value: int):
    return await tags.update_many({"_id": {"$in": id_list}}, {"$inc": {"counter": value}})