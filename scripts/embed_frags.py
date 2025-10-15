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
from tqdm import tqdm

from LRU_cache import LRUCache


dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path)

df = pd.read_csv("../data/fra_cleaned.csv", encoding="Windows-1252", sep=";")
df_sorted = df.sort_values(by="Rating Count", ascending=False)
df = df_sorted

unclean_df = pd.read_csv("../data/fra_perfumes.csv", encoding="utf-8", sep=",")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mongodb_client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))

EMBED_DIM = len(
    openai_client.embeddings.create(model="text-embedding-3-small", input=["test"])
    .data[0]
    .embedding
)


fragrance_db = mongodb_client["fragrance_db"]
fragrances_collection = fragrance_db["fragrances"]
accords_collection = fragrance_db["accords"]
notes_collection = fragrance_db["notes"]
brands_collection = fragrance_db["brands"]
countries_collection = fragrance_db["countries"]

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


def parseDescriptor(descriptor):
    extra_words = ["accord", "notes"]
    if descriptor in pretentiousDescriptors:
        return pretentiousDescriptors[descriptor]
    pattern = r"\b(?:" + "|".join(extra_words) + r")\b\.?$"
    cleaned = re.sub(pattern, "", descriptor, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"[\s,;]+$", "", cleaned)
    return cleaned


# Indexes
fragrances_collection.create_index([("brand", 1)])
fragrances_collection.create_index([("country", 1)])
fragrances_collection.create_index([("ratingCount", 1)])
fragrances_collection.create_index([("url", 1)], unique=True)

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
    # split only on commas that are not inside parentheses
    parts = re.split(r",\s*(?![^()]*\))", val)
    return [clean_note(x) for x in parts if x.strip()]


def safe_accords(url):
    try:
        row = unclean_df.loc[unclean_df["url"].str.lower() == url, "Main Accords"]
        if not row.empty:
            return [x.lower() for x in ast.literal_eval(str(row.iloc[0]))]
    except Exception:
        pass
    return []


def embed_list_cached(texts: list, note=True):
    vectors = []
    missing_texts = []
    collection = notes_collection if note else accords_collection
    for t in texts:
        v = (note_cache if note else accord_cache).get(t)
        if v is not None:
            vectors.append(np.array(v["embedding"]))
        else:
            doc = collection.find_one({"name": t}, {"_id": 1, "embedding": 1})
            if doc:
                (note_cache if note else accord_cache).put(
                    t,
                    {
                        "_id": doc["_id"],
                        "name": t,
                        "embedding": np.array(doc["embedding"]),
                    },
                )
            else:
                missing_texts.append(t)

    if missing_texts:
        response = openai_client.embeddings.create(
            model="text-embedding-3-small", input=missing_texts
        )
        embeddings = [np.array(x.embedding) for x in response.data]
        for t, e in zip(missing_texts, embeddings):
            result = collection.insert_one({"name": t, "embedding": e.tolist()})
            (note_cache if note else accord_cache).put(
                t, {"_id": result.inserted_id, "name": t, "embedding": e}
            )
        vectors.extend(embeddings)

    return vectors


def embed_text(text, note=True):
    v = (note_cache if note else accord_cache).get(text)
    if v is not None:
        return v["embedding"]
    else:
        response = openai_client.embeddings.create(
            model="text-embedding-3-small", input=text
        )
        embedding = np.array(response.data[0].embedding)
        return embedding


def get_descriptor_id(name: str, note=True):
    if not name:
        return None
    collection = notes_collection if note else accords_collection
    v = (note_cache if note else accord_cache).get(name)
    if v is not None:
        return v["_id"]
    doc = collection.find_one({"name": name}, {"_id": 1, "embedding": 1})
    if doc:
        (note_cache if note else accord_cache).put(
            name,
            {"_id": doc["_id"], "name": name, "embedding": np.array(doc["embedding"])},
        )
        return doc["_id"]
    embedding = embed_text(name, note=note)
    result = collection.insert_one({"name": name, "embedding": embedding.tolist()})
    (note_cache if note else accord_cache).put(
        name, {"_id": result.inserted_id, "name": name, "embedding": embedding}
    )
    return result.inserted_id


def accord_vector(accords):
    if not accords:
        return np.zeros(EMBED_DIM)
    weights = np.linspace(len(accords), 1, num=len(accords))
    weights /= weights.sum()
    vecs = np.array(embed_list_cached(accords, note=False))
    return np.sum(vecs * weights[:, np.newaxis], axis=0)


def average_embeddings(vectors, weight=1.0):
    if not vectors:
        return np.zeros(EMBED_DIM)
    return weight * np.mean(vectors, axis=0)


# --- Main embedding loop ---
print("Started Embedding")
start_time = time.time()

for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing fragrances"):
    url = safe_str(row.get("url"))
    if fragrances_collection.find_one({"url": url}):
        continue
    res = {}
    res["name"] = safe_str(row.get("Perfume"))
    res["url"] = url
    res["rating"] = safe_float(row.get("Rating Value"))
    res["ratingCount"] = safe_int(row.get("Rating Count"))
    res["year"] = safe_int(row.get("Year"))
    res["brand"] = safe_str(row.get("Brand"))
    res["gender"] = safe_str(row.get("Gender"))
    res["country"] = safe_str(row.get("Country"))

    res["topNotes"] = [
        get_descriptor_id(parseDescriptor(x)) for x in safe_list(row.get("Top"))
    ]
    res["midNotes"] = [
        get_descriptor_id(parseDescriptor(x)) for x in safe_list(row.get("Middle"))
    ]
    res["baseNotes"] = [
        get_descriptor_id(parseDescriptor(x)) for x in safe_list(row.get("Base"))
    ]
    res["accords"] = [
        get_descriptor_id(parseDescriptor(x), note=False)
        for x in safe_accords(res["url"])
    ]

    res["topNotesVector"] = average_embeddings(
        embed_list_cached([parseDescriptor(x) for x in safe_list(row.get("Top"))])
    ).tolist()
    res["midNotesVector"] = average_embeddings(
        embed_list_cached([parseDescriptor(x) for x in safe_list(row.get("Middle"))])
    ).tolist()
    res["baseNotesVector"] = average_embeddings(
        embed_list_cached([parseDescriptor(x) for x in safe_list(row.get("Base"))])
    ).tolist()

    res["totalNotesVector"] = (
        w_top * np.array(res["topNotesVector"])
        + w_mid * np.array(res["midNotesVector"])
        + w_base * np.array(res["baseNotesVector"])
    ).tolist()

    res["accordVector"] = accord_vector(
        [parseDescriptor(x) for x in safe_accords(res["url"])]
    ).tolist()
    res["fragranceVector"] = (
        w_notes * np.array(res["totalNotesVector"])
        + w_accords * np.array(res["accordVector"])
    ).tolist()

    # Update sets
    all_countries.add(res["country"])
    all_brands.add(res["brand"])

    # Upsert fragrance
    fragrances_collection.update_one(
        {"url": res["url"]}, {"$setOnInsert": res}, upsert=True
    )

# --- Bulk write for metadata ---
for collection, items in [
    (brands_collection, all_brands),
    (countries_collection, all_countries),
]:
    ops = [
        UpdateOne({"name": x}, {"$setOnInsert": {"name": x}}, upsert=True)
        for x in items
    ]
    collection.bulk_write(ops, ordered=False)

end_time = time.time()
print(f"✅ Processed {len(df)} fragrances in {end_time - start_time:.2f} seconds")


with open("../data/note_cache.json", "w") as f:
    json.dump(note_cache.to_dict(), f)

with open("../data/accord_cache.json", "w") as f:
    json.dump(accord_cache.to_dict(), f)

print("Caches saved to JSON files.")
