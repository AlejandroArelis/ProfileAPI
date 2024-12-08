from bson import ObjectId
from typing import List

from Player.repositories import people

async def get_by_id_list(id_list: List[ObjectId]):

    people_list = await people.get_by_id_list(id_list)

    for person in people_list:
        person["id"] = str(person["_id"])
        del person["_id"]

    return people_list