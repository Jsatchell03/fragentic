import json
import os
import numpy as np
from scipy.spatial.distance import cosine
from dotenv import load_dotenv
from openai import OpenAI
import time


dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
w_note_coverage, w_base_sim = 0.35, 0.65

# with open("../data/embedded_frags.json", "r") as f:
#     fragrances = json.load(f)

with open("../data/note_cache.json", "r") as f:
    note_cache = json.load(f)

with open("../data/accord_cache.json", "r") as f:
    accord_cache = json.load(f)


def cosine_similarity(vec1, vec2):
    return 1 - cosine(vec1, vec2)


def embed_list(texts: list):
    ai_response = [
        x.embedding
        for x in client.embeddings.create(
            model="text-embedding-3-small", input=texts
        ).data
    ]
    return ai_response


def embed_text(text: str):
    ai_response = [client.embeddings.create(model="text-embedding-3-small", input=text)]
    embedding = np.array(ai_response[0].data[0].embedding)
    return embedding


def average_embeddings(vectors, weight=1.0):
    if not vectors:
        return np.zeros(1536)  # dimension of text-embedding-3-small
    avg = np.mean(vectors, axis=0)
    return weight * avg


def note_coverage(q_vecs, f_vecs, threshold=0.5):
    matched = 0
    for qv in q_vecs:
        sims = [cosine_similarity(qv, fv) for fv in f_vecs]
        if max(sims) >= threshold:
            matched += 1
    return matched / len(q_vecs)


def find_perfume(fake_input, gender=None, top_n=5):
    similarities = []
    for f in fragrances:
        if gender and f["gender"] != gender:
            continue
        all_notes = f["topNotes"] + f["midNotes"] + f["baseNotes"]
        accords = f["accords"]
        note_vectors = [note_cache[note] for note in all_notes]
        accord_vectors = [accord_cache[accord] for accord in accords]
        sim = cosine_similarity(average_embeddings(fake_input), f["fragranceVector"])
        coverage = note_coverage(fake_input, (note_vectors + accord_vectors))
        score = (w_base_sim * sim) + (w_note_coverage * coverage)
        similarities.append((f["name"], f["brand"], score))

    similarities.sort(key=lambda x: x[2], reverse=True)

    return similarities[:top_n]


word1 = input("Enter word: ")
word2 = input("Enter word: ")
print(
    cosine_similarity(
        embed_text(word1),
        embed_text(word2),
    )
)
# query = input("Enter notes seperated by comas: ")
# gender_input = input("Gender: ")
# clean_query = [q.strip() for q in query.split(",")]
# print(clean_query)
# similar_perfumes = find_perfume(embed_list(clean_query), gender=gender_input, top_n=10)
# for name, brand, sim in similar_perfumes:
#     print(f"{name} ({brand}) - similarity: {sim:.4f}")
