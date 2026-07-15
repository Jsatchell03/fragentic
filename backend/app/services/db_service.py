from pymongo import MongoClient, InsertOne
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["fragentic"]


def dump(collection_name, documents):
    if collection_name not in db.list_collection_names():
        raise ValueError(f"[{collection_name}] does not exist in db.")

    db[collection_name].drop()

    collection = db[collection_name]
    ops = []
    for doc in documents:
        ops.append(InsertOne(doc))

    collection.bulk_write(ops)


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


def check_match(collection_name, query):
    if collection_name not in db.list_collection_names():
        raise ValueError(f"[{collection_name}] does not exist in db.")

    collection = db[collection_name]

    return collection.count_documents(query, limit=1) > 0
