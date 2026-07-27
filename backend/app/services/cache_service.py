from app.clients.redis_client import get, set, get_bytes, set_bytes, get_many_bytes, mset_bytes
import numpy as np


def get_descriptor(name: str):
    raw = get_bytes(f"descriptor:{name}")
    if raw is None:
        return None
    return np.frombuffer(raw, dtype=np.float32)


def get_descriptors(names):
    raw_bytes = get_many_bytes([f"descriptor:{name}" for name in names])
    results = []
    for raw in raw_bytes:
        if raw is not None:
            results.append(np.frombuffer(raw, dtype=np.float32))
        else:
            results.append(None)
    return results


def set_descriptor(name: str, vector):
    result = set_bytes(f"descriptor:{name}", vector.astype(np.float32).tobytes())
    return result


def set_descriptors(pairs: list[tuple]):
    mapping = {f"descriptor:{name}": vec.astype(np.float32).tobytes() for name, vec in pairs}
    mset_bytes(mapping)


def get_result(query: dict):
    pass


def set_result(query, results: list):
    pass


def get_fragrance(id):
    pass


def set_fragrance(fragrance):
    pass
