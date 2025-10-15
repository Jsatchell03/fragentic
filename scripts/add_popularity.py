from pymongo import MongoClient
import os
from dotenv import load_dotenv
import math
import time

from tqdm import tqdm


# Load environment variables
dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path)

# Connect to MongoDB
mongodb_client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
frag_db = mongodb_client["fragrance_db"]
fragrances = frag_db["fragrances"]

# Popularity weights
W_v = 0.7
W_R = 0.3
current_year = 2025

# First, get the max ratingCount in the collection for normalization
max_rating_count_doc = fragrances.find_one(sort=[("ratingCount", -1)])
V_max = max_rating_count_doc["ratingCount"] if max_rating_count_doc else 1
print(V_max)
# Iterate over all fragrances
# total_docs = fragrances.count_documents({})

# for i, frag in enumerate(tqdm(fragrances.find({}), total=total_docs)):
#     v = frag.get("ratingCount", 0)
#     R = frag.get("rating", 0)
#     name = frag.get("name", "")
#     year = frag.get("year", current_year)

#     # Popularity formula
#     popularity = (math.log(v + 1) / math.log(V_max + 1)) * W_v + (R / 5) * W_R
#     popularity = round(popularity, 3)
#     # Update the document
#     fragrances.update_one({"_id": frag["_id"]}, {"$set": {"popularity": popularity}})
#     if i % 100 == 0:
#         print(f"{i} documents processed, latest: {name} → {popularity}")

# print(f"Popularity updated for all {total_docs} fragrances.")

total_docs = fragrances.count_documents({})
start_time = time.time()
for i, frag in enumerate(tqdm(fragrances.find({}), total=total_docs)):
    v = frag.get("ratingCount", 0)
    R = frag.get("rating", 0)
    name = frag.get("name", "")
    year = frag.get("year", current_year)

    # Popularity formula
    popularity = (math.log(v + 1) / math.log(V_max + 1)) * W_v + (R / 5) * W_R
    popularity = round(popularity, 3)
    # Update the document
    fragrances.update_one({"_id": frag["_id"]}, {"$set": {"popularity": popularity}})
    if i % 1000 == 0:
        curr_time = time.time()
        print(
            f"{i} documents processed in {curr_time - start_time:.2f} seconds, latest: {name} → {popularity}"
        )

print(f"Popularity updated for all {total_docs} fragrances.")
