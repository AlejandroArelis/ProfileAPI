from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb+srv://profile_user:tReN6duf2i8LSwesec7Y4y5jOFuQeChu6RiStofinAfiPItlw3peWRIthU4eMi3T@micluster.wzbs7ki.mongodb.net/")
db = client["profile"]