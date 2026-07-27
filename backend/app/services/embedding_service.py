from app.clients.openai_client import get_embedding, get_many_embeddings
from app.services.cache_service import get_descriptor, set_descriptor, get_descriptors, set_descriptors
from app.config import settings
import numpy as np

EMBED_DIM = settings.openai.dimensions


def embed_descriptors(descriptors: list[str]):
    if not descriptors:
        return []
    results = get_descriptors(descriptors)
    misses = [(i, descriptors[i]) for i, r in enumerate(results) if r is None]
    if misses:
        vectors = get_many_embeddings([m[1] for m in misses])
        set_descriptors([(misses[i][1], vectors[i]) for i in range(len(misses))])
        for i, (idx, _) in enumerate(misses):
            results[idx] = vectors[i]
    return results


def embed(text: str):
    cached = get_descriptor(text)
    if cached is None:
        return get_embedding(text)
    return cached


def avg_embeddings(notes, weight=1.0):
    if not notes:
        return np.zeros(EMBED_DIM)
    vectors = embed_descriptors(notes)
    return weight * np.mean(vectors, axis=0)


def cosine_sim(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)

    # Compute cosine similarity
    similarity = dot_product / (norm_a * norm_b)
    return similarity
