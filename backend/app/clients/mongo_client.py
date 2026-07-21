from pymongo import MongoClient, InsertOne
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["fragentic"]


def upload_one(collection_name: str, document: dict):
    if collection_name not in db.list_collection_names():
        raise ValueError(f"[{collection_name}] does not exist in db.")

    collection = db[collection_name]
    response = collection.insert_one(document)

    return response.inserted_id


def get_all(collection_name: str) -> list:
    if collection_name not in db.list_collection_names():
        raise ValueError(f"[{collection_name}] does not exist in db.")

    collection = db[collection_name]
    documents = list(collection.find({}))

    return documents


def query_collection(collection_name, query):
    if collection_name not in db.list_collection_names():
        raise ValueError(f"[{collection_name}] does not exist in db.")
    collection = db[collection_name]
    documents = list(collection.find(query))
    if not documents:
        return None

    return documents


print(get_all("descriptors"))
