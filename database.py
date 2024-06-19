import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
load_dotenv()
client = AsyncIOMotorClient(f"mongodb+srv://{os.getenv("MONGODB_USER")}:{os.getenv("MONGODB_USER_PASSWORD")}@micluster.wzbs7ki.mongodb.net/")
db = client[os.getenv("MONGODB_DB")]