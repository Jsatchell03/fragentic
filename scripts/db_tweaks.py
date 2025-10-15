from pymongo import MongoClient
import os
from dotenv import load_dotenv
import numpy as np
from openai import OpenAI


dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path)
mongodb_client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

frag_db = mongodb_client["fragrance_db"]

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

# Add vector to notes and accords
# import numpy as np
# import time


# db = mongodb_client["fragrance_db"]
# notes_collection = db["notes"]
# accords_collection = db["accords"]
# start_time = time.time()
# for note in list(notes_collection.find({})):
#     if "embedding" in note:
#         continue
#     print(f"Embedding {note["name"]}")
#     response = openai_client.embeddings.create(
#         model="text-embedding-3-small", input=note["name"]
#     )
#     embedding = response.data[0].embedding
#     notes_collection.update_one(
#         {"_id": note["_id"]}, {"$set": {"embedding": embedding}}
#     )
# end_time = time.time()

# print(f"Embedding took {end_time - start_time:.2f} seconds")

# Add descriptors field

# from bson import ObjectId
# from tqdm import tqdm

# # --- CONFIG ---
# db = mongodb_client["fragrance_db"]

# fragrances = db.fragrances
# notes_col = db.notes
# accords_col = db.accords

# # --- SCRIPT ---
# # Query only fragrances missing the descriptors field (for incremental updates)
# cursor = fragrances.find({"descriptors": {"$exists": False}})

# for frag in tqdm(cursor, desc="Updating fragrances"):
#     descriptor_ids = {
#         "accords": [],
#         "topNotes": [],
#         "midNotes": [],
#         "baseNotes": [],
#     }

#     # Collect ObjectIds by category
#     for field in descriptor_ids.keys():
#         if field in frag and isinstance(frag[field], list):
#             descriptor_ids[field].extend([ObjectId(x) for x in frag[field]])

#     # --- Look up names from each collection ---
#     accord_names = []
#     if descriptor_ids["accords"]:
#         accord_docs = accords_col.find(
#             {"_id": {"$in": descriptor_ids["accords"]}}, {"name": 1}
#         )
#         accord_names = [doc["name"] for doc in accord_docs if "name" in doc]

#     note_names = []
#     note_fields = ["topNotes", "midNotes", "baseNotes"]
#     note_ids = sum((descriptor_ids[f] for f in note_fields), [])
#     if note_ids:
#         note_docs = notes_col.find({"_id": {"$in": note_ids}}, {"name": 1})
#         note_names = [doc["name"] for doc in note_docs if "name" in doc]

#     # Combine and deduplicate all descriptors
#     descriptors = sorted(set(accord_names + note_names))

#     # --- Update fragrance document ---
#     fragrances.update_one({"_id": frag["_id"]}, {"$set": {"descriptors": descriptors}})

#     tqdm.write(
#         f"Updated {frag.get('name', frag['_id'])} ({len(descriptors)} descriptors)"
#     )


# clean up notes and accords

pretentiousDescriptors = {
    "wild lavender": "lavender",
    "citruses": "citrus",
    "woodsy notes": "wood",
    "sweet notes": "sweet",
    "green accord": "green",
    "cedar essence": "cedar",
    "cedarwood": "cedar",
    "california orange": "orange",
    "oriental notes": "oriental notes",
    "mastic or lentisque": "mastic",
    "mandarin": "mandarin orange",
    "calabrian mandarin": "italian mandarin",
    "sicilian mandarin": "italian mandarin",
    "lily-of-the-valley": "lily of the valley",
    "american apple": "apple",
    "citrus leaf": "citrus leaves",
    "citruses water": "citrus water",
    "citruses with sugar": "sweet citrus",
    "sicilian citruses": "sicilian citrus",
    "cornflower or sultan seeds": "cornflower/sweet sultan seeds",
    "arbutus (madrona, bearberry tree)": "arbutus (madrone/bearberry tree)",
    "agathosma betulina": "agathosma betulina (buchu)",
    "cubeb or tailed pepper": "tailed pepper (cubeb)",
    "christmas tree or flame tree": "flame tree",
    "melilot or sweet clover": "sweet clover (meliot)",
    "woodruff or galium odoratum": "sweet woodruff (galium odoratum)",
    "hamanasu or japanese rose": "japanese rose (hamanasu)",
    "portulaca or pigweed": "portulaca (pigweed)",
    "silk vine or milk broom": "periploca (milk broom/silk vine)",
    "pepperwood or hercules club": "hercules club (pepperwood)",
    "zanthoxylum clava-herculis": "hercules club (pepperwood)",
    "cypriol oil or nagarmotha": "cypriol oil (nagarmotha)",
    "chimonanthus or wintersweet": "chimonanthus (wintersweet)",
    "black hemlock or tsuga": "black hemlock (tsuga mertensiana)",
    "princess tree or paulownia": "princess tree (paulownia tomentosa)",
    "dark woodsy": "dark wood",
    "pepperwood™": "pepperwood",
    "white woods": "white wood",
    "oriental woodsy": "oriental woods",
    "woody": "wood",
    "coton candy": "cotton candy",
    "pine": "pine tree",
    "virginian cedar": "virginia cedar",
    "apple tree blossom": "apple blossom",
    "vanila": "vanilla",
}

notes_col = frag_db["notes"]
accords_col = frag_db["accords"]
fragrances_col = frag_db["fragrances"]
DRY_RUN = False  # True = don't update MongoDB, just print actions
TEST_LIMIT = None


# def update_collection_and_fragrances(collection, array_fields):
#     for old_name, new_name in pretentiousDescriptors.items():
#         old_doc = collection.find_one({"name": old_name})
#         if not old_doc:
#             continue

#         new_doc = collection.find_one({"name": new_name})
#         if new_doc:
#             new_id = new_doc["_id"]
#             print(f"Reusing existing ID for {new_name}")
#         else:
#             response = openai_client.embeddings.create(
#                 model="text-embedding-3-small", input=new_name
#             )
#             embedding = response.data[0].embedding
#             if not DRY_RUN:
#                 collection.update_one(
#                     {"_id": old_doc["_id"]},
#                     {"$set": {"name": new_name, "embedding": embedding}},
#                 )
#             new_id = old_doc["_id"]
#             print(f"Renamed {old_name} -> {new_name} with new embedding")

#         # Update fragrance arrays
#         for field in array_fields:
#             if not DRY_RUN:
#                 fragrances_col.update_many(
#                     {field: old_doc["_id"]},
#                     {"$set": {f"{field}.$[elem]": new_id}},
#                     array_filters=[{"elem": old_doc["_id"]}],
#                 )
#             print(
#                 f"Updated fragrance array '{field}' replacing {old_doc['_id']} with {new_id}"
#             )

#         # Update descriptors array
#         if not DRY_RUN:
#             fragrances_col.update_many(
#                 {"descriptors": old_name},
#                 {"$set": {"descriptors.$[elem]": new_name}},
#                 array_filters=[{"elem": old_name}],
#             )
#         print(f"Updated descriptors replacing '{old_name}' with '{new_name}'")


# # --- Update Notes ---
# print("=== UPDATING NOTES ===")
# update_collection_and_fragrances(notes_col, ["topNotes", "midNotes", "baseNotes"])

# # --- Update Accords ---
# print("\n=== UPDATING ACCORDS ===")
# update_collection_and_fragrances(accords_col, ["accords"])

# # --- Deduplicate descriptors per fragrance ---
# cursor = fragrances_col.find({})
# if TEST_LIMIT:
#     cursor = cursor.limit(TEST_LIMIT)

# for frag in cursor:
#     descriptors = frag.get("descriptors", [])
#     unique_descriptors = list(set(descriptors))
#     if descriptors != unique_descriptors:
#         if not DRY_RUN:
#             fragrances_col.update_one(
#                 {"_id": frag["_id"]}, {"$set": {"descriptors": unique_descriptors}}
#             )
#         print(
#             f"Deduplicated descriptors for fragrance {frag.get('name', frag['_id'])}: {unique_descriptors}"
#         )

# print("\n✅ Full run complete. All notes, accords, and descriptors updated.")

keys_to_delete = list(pretentiousDescriptors.keys())

# --- Delete from notes ---
result_notes = notes_col.delete_many({"name": {"$in": keys_to_delete}})
print(f"Deleted {result_notes.deleted_count} notes.")

# --- Delete from accords ---
result_accords = accords_col.delete_many({"name": {"$in": keys_to_delete}})
print(f"Deleted {result_accords.deleted_count} accords.")
