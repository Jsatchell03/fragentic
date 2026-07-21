from app.clients.openai_client import get_embedding, get_many_embeddings
from app.clients.redis_client import get_descriptor, set_descriptor
from app.clients.mongo_client import query_collection
import numpy as np


def embed_descriptors(list: list[str]):
    results = []
    for element in list:
        cached = get_descriptor(element)
        if cached:
            results.append(cached)
            continue
        stored = query_collection("descriptors", {"name": element})
        if stored:
            results.append(stored)
            continue
        results.append(get_embedding(element))


def embed(text: str):
    cached = get_descriptor(text)
    if cached:
        return cached

    return get_embedding(text)


def avg_embeddings(list, weight=1.0):
    vectors = embed_descriptors(list)
    return weight * np.mean(vectors, axis=0)
