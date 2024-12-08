import os
from motor.motor_asyncio import AsyncIOMotorClient

# client = AsyncIOMotorClient(f"mongodb+srv://{os.getenv('MONGODB_USER')}:{os.getenv('MONGODB_USER_PASSWORD')}@micluster.wzbs7ki.mongodb.net/")
client = AsyncIOMotorClient(f"mongodb://localhost:27017/")