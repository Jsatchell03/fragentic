from app.clients import openai_client
from app.services import cache_service
from app.config import settings
from app.schemas.app_schemas import Descriptor
from app.services import mongo_service
import numpy as np

EMBED_DIM = settings.openai.dimensions


def l2_normalize(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


async def embed_descriptors(descriptors: list[str]):
    resolved: dict[str, Descriptor] = {}
    hits, misses = await cache_service.get_descriptors(descriptors)
    for d in hits:
        resolved[d.name] = d

    if misses:
        stored_names = []
        new_names = []
        for name in misses:
            if name in mongo_service.STORED_DESCRIPTOR_NAMES:
                stored_names.append(name)
            else:
                new_names.append(name)

        uncached: list[Descriptor] = []

        if stored_names:
            for d in await mongo_service.find_descriptors(stored_names):
                resolved[d.name] = d
                uncached.append(d)

        if new_names:
            new_vectors = await openai_client.get_many_embeddings(new_names)
            for name, vector in zip(new_names, new_vectors):
                d = Descriptor(name=name, list_vector=vector)
                resolved[name] = d
                uncached.append(d)

        await cache_service.set_descriptors(uncached)

    return [resolved[name] for name in descriptors]


async def embed(text: str):
    return await openai_client.get_embedding(text)


def avg_vectors(vectors, weight=1.0):
    if not vectors:
        return np.zeros(EMBED_DIM)
    avg = weight * np.mean(vectors, axis=0)
    return avg


def cosine_sim(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    similarity = dot_product / (norm_a * norm_b)
    return similarity
