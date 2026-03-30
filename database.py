from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "micro_learning"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# Collections
users_collection = db["users"]
lessons_collection = db["lessons"]
progress_collection = db["progress"]
sessions_collection = db["sessions"]
badges_collection = db["badges"]
quests_collection = db["quests"]
