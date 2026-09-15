from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client["fragentic"]


async def upload_one(collection_name: str, document: dict):
    if collection_name not in await db.list_collection_names():
        raise ValueError(f"[{collection_name}] does not exist in db.")
    collection = db[collection_name]
    response = await collection.insert_one(document)
    return response.inserted_id


async def upload_many(collection_name: str, documents: list[dict]):
    if collection_name not in await db.list_collection_names():
        raise ValueError(f"[{collection_name}] does not exist in db.")
    collection = db[collection_name]
    await collection.insert_many(documents, ordered=False)


async def get_all(collection_name: str) -> list:
    if collection_name not in await db.list_collection_names():
        raise ValueError(f"[{collection_name}] does not exist in db.")
    collection = db[collection_name]
    return await collection.find({}).to_list(None)


async def query_collection(collection_name, query, projection=None):
    if collection_name not in await db.list_collection_names():
        raise ValueError(f"[{collection_name}] does not exist in db.")
    collection = db[collection_name]
    if projection:
        documents = await collection.find(query, projection).to_list(None)
    else:
        documents = await collection.find(query).to_list(None)
    if not documents:
        return None
    return documents


async def execute_pipeline(collection_name, pipeline):
    if collection_name not in await db.list_collection_names():
        raise ValueError(f"[{collection_name}] does not exist in db.")
    return await db[collection_name].aggregate(pipeline).to_list(None)
