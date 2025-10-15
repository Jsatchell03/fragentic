from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path)

# Connect to MongoDB
mongodb_client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
frag_db = mongodb_client["fragrance_db"]
fragrances = frag_db["fragrances"]

# Aggregation pipeline to find most common descriptors
pipeline = [
    {"$unwind": "$descriptors"},  # Flatten the descriptors array
    {"$group": {"_id": "$descriptors", "count": {"$sum": 1}}},  # Count each descriptor
    {"$sort": {"count": -1}},  # Sort by count descending
    {"$limit": 50},  # Keep top 10
]

results = list(fragrances.aggregate(pipeline))
res = []
print("Top 10 most common descriptors:")
for doc in results:
    res.append(doc["_id"])

print(res)
