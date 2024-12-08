from bson import ObjectId
from typing import List
from Player.db.mongo import db

people = db["people"]

async def save(name):
    new = await people.insert_one({"name": name, "counter": 1})
    return await get_by_id(new.inserted_id)

async def get_by_id(id: ObjectId):
    tag = await people.find_one({"_id": id})

    if tag:
        tag["id"] = str(tag["_id"])
        del tag["_id"]

    return tag

async def get_by_name(name):
    tag = await people.find_one({"name": name})

    if tag:
        tag["id"] = str(tag["_id"])
        del tag["_id"]

    return tag

async def get_by_id_list(id_list: List[ObjectId]):
    return await people.find({"_id": {"$in": id_list}}).to_list(None)

async def set_counter(id_list: List[ObjectId], value: int):
    return await people.update_many({"_id": {"$in": id_list}}, {"$inc": {"counter": value}})