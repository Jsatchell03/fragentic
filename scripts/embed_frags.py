import pandas as pd
import numpy as np
import json
from openai import OpenAI
import time
import os
import re
import ast
from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne
from LRU_cache import LRUCache

dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path)

df = pd.read_csv("../data/fra_cleaned.csv", encoding="Windows-1252", sep=";")
df_sorted = df.sort_values(by="Rating Count", ascending=False)
df = df_sorted[:1000]

unclean_df = pd.read_csv("../data/fra_perfumes.csv", encoding="utf-8", sep=",")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mongodb_client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))

fragrences_db = mongodb_client["fragrences_db"]
fragrences_collection = fragrences_db["fragrences"]
accords_collection = fragrences_db["accords"]
notes_collection = fragrences_db["notes"]
brands_collection = fragrences_db["brands"]
countries_collection = fragrences_db["countries"]

# Indexes
fragrences_collection.create_index({"brand": 1})
fragrences_collection.create_index({"country": 1})
fragrences_collection.create_index({"ratingCount": 1})
fragrences_collection.create_index("url", unique=True)

w_top, w_mid, w_base = 0.25, 0.30, 0.45
w_notes, w_accords = 0.4, 0.6

# Initialize caches

with open("../data/note_cache.json", "r") as f:
    note_cache_data = json.load(f)

with open("../data/accord_cache.json", "r") as f:
    accord_cache_data = json.load(f)

note_cache = LRUCache(note_cache_data)
accord_cache = LRUCache(accord_cache_data)


# Existing sets
all_brands = set(brands_collection.distinct("name"))
all_countries = set(countries_collection.distinct("name"))
all_notes = set(notes_collection.distinct("name"))
all_accords = set(accords_collection.distinct("name"))


# --- Helper functions ---
def safe_str(val):
    return str(val).lower().strip() if pd.notna(val) else ""


def safe_float(val, default=0.0):
    try:
        return float(str(val).replace(",", ".")) if pd.notna(val) else default
    except Exception:
        return default


def safe_int(val, default=0):
    try:
        return int(val) if pd.notna(val) else default
    except Exception:
        return default


def clean_note(text: str) -> str:
    text = text.strip().lower()
    match = re.search(r"\((.*?)\)", text)
    return match.group(1).strip() if match else text


def safe_list(val):
    if pd.isna(val) or not isinstance(val, str):
        return []
    return [clean_note(x) for x in val.split(",") if x.strip()]


def safe_accords(url):
    try:
        row = unclean_df.loc[unclean_df["url"].str.lower() == url, "Main Accords"]
        if not row.empty:
            return ast.literal_eval(str(row.iloc[0]).lower())
    except Exception:
        pass
    return []


def embed_list_cached(texts: list, note=True):
    vectors = []
    missing_texts = []
    for t in texts:
        v = (note_cache if note else accord_cache).get(t)
        if v is not None:
            vectors.append(v)
        else:
            missing_texts.append(t)

    if missing_texts:
        response = openai_client.embeddings.create(
            model="text-embedding-3-small", input=missing_texts
        )
        embeddings = [np.array(x.embedding) for x in response.data]
        for t, e in zip(missing_texts, embeddings):
            (note_cache if note else accord_cache).put(t, e)
        vectors.extend(embeddings)

    return vectors


def accord_vector(accords):
    if not accords:
        return np.zeros(1536)
    weights = np.linspace(len(accords), 1, num=len(accords))
    weights /= weights.sum()
    vecs = np.array(embed_list_cached(accords, note=False))
    return np.sum(vecs * weights[:, np.newaxis], axis=0)


def average_embeddings(vectors, weight=1.0):
    if not vectors:
        return np.zeros(1536)
    return weight * np.mean(vectors, axis=0)


# --- Main embedding loop ---
print("Started Embedding")
start_time = time.time()

for _, row in df.iterrows():
    res = {}
    res["name"] = safe_str(row.get("Perfume"))
    res["url"] = safe_str(row.get("url"))
    res["rating"] = safe_float(row.get("Rating Value"))
    res["ratingCount"] = safe_int(row.get("Rating Count"))
    res["year"] = safe_int(row.get("Year"))
    res["brand"] = safe_str(row.get("Brand"))
    res["gender"] = safe_str(row.get("Gender"))
    res["country"] = safe_str(row.get("Country"))

    res["topNotes"] = safe_list(row.get("Top"))
    res["midNotes"] = safe_list(row.get("Middle"))
    res["baseNotes"] = safe_list(row.get("Base"))
    res["accords"] = safe_accords(res["url"])

    res["topNotesVector"] = average_embeddings(
        embed_list_cached(res["topNotes"])
    ).tolist()
    res["midNotesVector"] = average_embeddings(
        embed_list_cached(res["midNotes"])
    ).tolist()
    res["baseNotesVector"] = average_embeddings(
        embed_list_cached(res["baseNotes"])
    ).tolist()

    res["totalNotesVector"] = (
        w_top * np.array(res["topNotesVector"])
        + w_mid * np.array(res["midNotesVector"])
        + w_base * np.array(res["baseNotesVector"])
    ).tolist()

    res["accordVector"] = accord_vector(res["accords"]).tolist()
    res["fragranceVector"] = (
        w_notes * np.array(res["totalNotesVector"])
        + w_accords * np.array(res["accordVector"])
    ).tolist()

    # Update sets
    all_countries.add(res["country"])
    all_brands.add(res["brand"])
    all_notes.update(res["topNotes"])
    all_notes.update(res["midNotes"])
    all_notes.update(res["baseNotes"])
    all_accords.update(res["accords"])

    # Upsert fragrance
    fragrences_collection.update_one(
        {"url": res["url"]}, {"$setOnInsert": res}, upsert=True
    )
    print(f"{res["name"]} added")

# --- Bulk write for metadata ---
for collection, items in [
    (brands_collection, all_brands),
    (countries_collection, all_countries),
    (notes_collection, all_notes),
    (accords_collection, all_accords),
]:
    ops = [
        UpdateOne({"name": x}, {"$setOnInsert": {"name": x}}, upsert=True)
        for x in items
    ]
    collection.bulk_write(ops, ordered=False)

end_time = time.time()
print(f"Embedding took {end_time - start_time:.2f} seconds")


with open("../data/note_cache.json", "w") as f:
    json.dump(note_cache.to_dict(), f)

with open("../data/accord_cache.json", "w") as f:
    json.dump(accord_cache.to_dict(), f)

print("Caches saved to JSON files.")
