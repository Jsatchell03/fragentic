from openai import OpenAI
import os
from dotenv import load_dotenv
from app.config import settings

load_dotenv()
client = OpenAI()
MODEL = settings.openai.model

CACHE_MAX_SIZE = settings.etl.cache_max_size
BATCH_SIZE = settings.etl.batch_size

cache: dict[str, list[float]] = {}


def _cache_put(text: str, embedding: list[float]) -> None:
    if len(cache) < CACHE_MAX_SIZE:
        cache[text] = embedding


def get_embedding(text: str) -> list[float]:
    if text in cache:
        return cache[text]

    response = client.embeddings.create(input=text, model=MODEL)
    embedding = response.data[0].embedding
    _cache_put(text, embedding)
    return embedding


def get_many_embeddings(texts: list[str]) -> list[list[float]]:
    results: list[list[float] | None] = [cache.get(t) for t in texts]
    miss_indices = [i for i, e in enumerate(results) if e is None]

    if miss_indices:
        miss_texts = [texts[i] for i in miss_indices]
        for start in range(0, len(miss_texts), BATCH_SIZE):
            chunk = miss_texts[start : start + BATCH_SIZE]
            chunk_indices = miss_indices[start : start + BATCH_SIZE]

            response = client.embeddings.create(input=chunk, model=MODEL)
            for idx, obj in zip(chunk_indices, response.data):
                results[idx] = obj.embedding
                _cache_put(texts[idx], obj.embedding)

    return results
