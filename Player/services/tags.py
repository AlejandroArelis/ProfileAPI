from bson import ObjectId
from typing import List

from Player.repositories import tags

async def get_by_id_list(id_list: List[ObjectId]):

    print("id_list", id_list)

    tags_list = await tags.get_by_id_list(id_list)

    print(tags_list)

    for tag in tags_list:
        tag["id"] = str(tag["_id"])
        del tag["_id"]

    return tags_list