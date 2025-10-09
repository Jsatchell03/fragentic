import pandas as pd
import numpy as np
import json
from openai import OpenAI
import time
import os
import re
import ast
from dotenv import load_dotenv


dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path)

df = pd.read_csv("../data/fra_cleaned.csv", encoding="Windows-1252", sep=";")
df_sorted = df.sort_values(by="Rating Count", ascending=False)
df = df_sorted[:100]

unclean_df = pd.read_csv("../data/fra_perfumes.csv", encoding="utf-8", sep=",")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
w_top, w_mid, w_base = 0.25, 0.30, 0.45
w_notes, w_accords = 0.4, 0.6

data = []
note_cache = accord_cache = {}
with open("../data/note_cache.json", "r") as f:
    note_cache = json.load(f)
with open("../data/accord_cache.json", "r") as f:
    accord_cache = json.load(f)


def check_cache(key, note=True):
    if not note:
        if key in accord_cache:
            print(f"Cache hit {key}")
            return accord_cache[key]
        else:
            print(f"Cache miss {key}")
            return -1

    if key in note_cache:
        print(f"Cache hit {key}")
        return note_cache[key]
    else:
        print(f"Cache miss {key}")
        return -1


def update_cache(key, val, note=True):
    if not note:
        accord_cache[key] = val
    else:
        note_cache[key] = val


def embed_text(text):
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return np.array(response.data[0].embedding)


def embed_list(texts: list, notes=True):
    res = []
    cache_misses = []
    for text in texts:
        cache = check_cache(text, notes)
        if cache != -1:
            res.append(cache)
        else:
            cache_misses.append(text)
    if len(cache_misses) == 0:
        return res

    ai_response = [
        x.embedding
        for x in client.embeddings.create(
            model="text-embedding-3-small", input=cache_misses
        ).data
    ]
    for i in range(len(cache_misses)):
        update_cache(cache_misses[i], ai_response[i], notes)
    res.extend(ai_response)

    return res


def accord_vector(accords):
    if not accords:
        return np.zeros(1536)

    weights = np.linspace(len(accords), 1, num=len(accords))
    weights = weights / weights.sum()

    vecs = embed_list(accords, False)
    vecs = np.array(vecs)
    weighted_vec = np.sum(vecs * weights[:, np.newaxis], axis=0)

    return weighted_vec


def average_embeddings(vectors, weight=1.0):
    if not vectors:
        return np.zeros(1536)  # dimension of text-embedding-3-small
    avg = np.mean(vectors, axis=0)
    return weight * avg


def clean_note(text: str) -> str:
    """Return only text inside parentheses if present, else the original."""
    text = text.strip().lower()
    match = re.search(r"\((.*?)\)", text)
    if match:
        return match.group(1).strip()
    return text


print("Started Embedding")
start_time = time.time()
for index, row in df.iterrows():
    row_dict = row.to_dict()
    res = {}
    res["name"] = row_dict["Perfume"].lower()
    res["url"] = row_dict["url"].lower()
    res["rating"] = row_dict["Rating Value"].replace(",", ".")
    res["brand"] = row_dict["Brand"].lower()
    res["gender"] = row_dict["Gender"].lower()
    res["country"] = row_dict["Country"].lower()
    res["topNotes"] = [clean_note(x) for x in row_dict["Top"].split(",") if x.strip()]
    res["midNotes"] = [
        clean_note(x) for x in row_dict["Middle"].split(",") if x.strip()
    ]
    res["baseNotes"] = [clean_note(x) for x in row_dict["Base"].split(",") if x.strip()]
    res["accords"] = ast.literal_eval(
        str(
            unclean_df.loc[
                unclean_df["url"].str.lower() == res["url"], "Main Accords"
            ].iloc[0]
        ).lower()
    )
    # Vectors
    res["topNotesVector"] = average_embeddings(embed_list(res["topNotes"])).tolist()
    res["midNotesVector"] = average_embeddings(embed_list(res["midNotes"])).tolist()
    res["baseNotesVector"] = average_embeddings(embed_list(res["baseNotes"])).tolist()
    # Weighted total notes vector
    res["totalNotesVector"] = (
        w_top * np.array(res["topNotesVector"])
        + w_mid * np.array(res["midNotesVector"])
        + w_base * np.array(res["baseNotesVector"])
    ).tolist()
    res["accordVector"] = accord_vector(res["accords"]).tolist()
    res["fragranceVector"] = (
        (w_notes * np.array(res["totalNotesVector"]))
        + (w_accords * np.array(res["accordVector"]))
    ).tolist()
    data.append(res)

with open("../data/embedded_frags.json", "w") as f:
    json.dump(data, f, indent=4)

with open("../data/note_cache.json", "w") as f:
    json.dump(note_cache, f, indent=4)

with open("../data/accord_cache.json", "w") as f:
    json.dump(accord_cache, f, indent=4)

all_notes = []
all_notes = list(set(note_cache.keys()) | set(accord_cache.keys()))
with open("../data/notes.json", "w") as f:
    json.dump(all_notes, f, indent=4)

end_time = time.time()
elapsed = end_time - start_time
print(f"Embedding took {elapsed:.2f} seconds")
