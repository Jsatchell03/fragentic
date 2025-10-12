from pymongo import MongoClient
import os
from dotenv import load_dotenv

dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path)
mongodb_client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))

# Fix "fragrences" collection typo
# db = mongodb_client["fragrences_db"]
# db["fragrences"].rename("fragrances")

# Fix "fragrences_db" typo
# old_db = mongodb_client["fragrences_db"]
# new_db = mongodb_client["fragrance_db"]

# for name in old_db.list_collection_names():
#     old_collection = old_db[name]
#     new_collection = new_db[name]
#     docs = list(old_collection.find({}))
#     if docs:
#         new_collection.insert_many(docs)
