from app.clients.redis_client import (
    get,
    set,
    get_bytes,
    set_bytes,
    get_many_bytes,
    mset_bytes,
)
import numpy as np

from app.schemas.app_schemas import Descriptor
from app.config import settings

VECTOR_DIM = settings.openai.dimensions


def vector_to_bytes(vector) -> bytes:
    return np.asarray(vector, dtype=np.float32).tobytes()


def bytes_to_vector(raw: bytes | None) -> list[float] | None:
    if raw is None:
        return None
    arr = np.frombuffer(raw, dtype=np.float32)
    if arr.shape[0] != VECTOR_DIM:
        raise ValueError(f"expected {VECTOR_DIM} floats, got {arr.shape[0]}")
    return arr.tolist()


async def get_many_vectors(keys) -> list[list[float] | None]:
    raw_results = await get_many_bytes(keys)
    return [bytes_to_vector(raw) for raw in raw_results]


async def get_descriptor(name: str):
    raw = await get_bytes(f"descriptor:{name}")
    if raw is None:
        return None
    vector = bytes_to_vector(raw)
    return Descriptor(name=name, list_vector=vector)


async def get_descriptors(names):
    raw_bytes = await get_many_bytes([f"descriptor:{name}" for name in names])
    hits = []
    misses = []
    for i in range(len(raw_bytes)):
        if raw_bytes[i] is not None:
            hits.append(
                Descriptor(name=names[i], list_vector=bytes_to_vector(raw_bytes[i]))
            )
        else:
            misses.append(names[i])
    return (hits, misses)


async def set_descriptor(descriptor: Descriptor):
    return await set_bytes(f"descriptor:{descriptor.name}", descriptor.np_vector.tobytes())


async def set_descriptors(descriptors: list[Descriptor]):
    mapping = {
        f"descriptor:{descriptor.name}": descriptor.np_vector.tobytes()
        for descriptor in descriptors
    }
    await mset_bytes(mapping)
