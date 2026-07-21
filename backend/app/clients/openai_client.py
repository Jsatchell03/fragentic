from openai import OpenAI
import os
from dotenv import load_dotenv
from app.config import settings
import numpy as np

load_dotenv()
client = OpenAI()
MODEL = settings.openai.model
BATCH_SIZE = settings.etl.batch_size
DIMENSIONS = settings.etl.dimensions


def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(input=text, model=MODEL, dimensions=DIMENSIONS)
    raw_vector = response.data[0].embedding
    return np.array(raw_vector, dtype=np.float32)


def get_many_embeddings(texts: list[str]) -> list[list[float]]:
    results = []

    for start in range(0, len(texts), BATCH_SIZE):
        chunk = texts[start : start + BATCH_SIZE]
        response = client.embeddings.create(
            input=chunk, model=MODEL, dimensions=DIMENSIONS
        )
        for obj in response.data:
            results.append(np.array(obj.embedding, dtype=np.float32))

    return results
