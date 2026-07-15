from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["fragentic"]


def bulk_upload(collection, documents):
    pass


def upload_one(collection_name: str, document: dict):
    if collection_name not in db.list_collection_names():
        raise ValueError(f"[{collection_name}] does not exist in db.")

    collection = db[collection_name]
    collection.insert_one(document)


def get_all(collection_name: str) -> list:
    if collection_name not in db.list_collection_names():
        raise ValueError(f"[{collection_name}] does not exist in db.")

    collection = db[collection_name]
    documents = list(collection.find({}))

    return documents
