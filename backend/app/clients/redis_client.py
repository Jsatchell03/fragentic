import os
from dotenv import load_dotenv
import redis
import numpy as np
import json
from app.config import settings

load_dotenv()

r = redis.Redis(
    host="localhost", port=6379, password=os.getenv("REDIS_PW"), decode_responses=False
)

KEY_PREFIX = settings.redis.key_prefix


def get(key):
    key = KEY_PREFIX + key
    result = r.get(key)
    if result is None:
        return None
    return json.loads(result)


def get_many_bytes(keys):
    results = r.mget([f"{KEY_PREFIX}{key}" for key in keys])
    return results


def get_bytes(key):
    key = KEY_PREFIX + key
    result = r.get(key)
    if result is None:
        return None
    return result


def set(key, value):
    key = KEY_PREFIX + key
    result = r.set(key, json.dumps(value))
    return result


def set_bytes(key, value):
    key = KEY_PREFIX + key
    result = r.set(key, value)
    return result


def mset_bytes(mapping: dict):
    prefixed = {f"{KEY_PREFIX}{k}": v for k, v in mapping.items()}
    r.mset(prefixed)
