import motor.motor_asyncio
import config

client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGODB_URI)
db = client["ai_music_bot"]
whitelist = db["whitelist"]

async def get_whitelist():
    users = await whitelist.find({}).to_list(length=1000)
    return [u["user_id"] for u in users]

async def add_to_whitelist(user_id: int):
    await whitelist.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

async def remove_from_whitelist(user_id: int):
    await whitelist.delete_one({"user_id": user_id})
