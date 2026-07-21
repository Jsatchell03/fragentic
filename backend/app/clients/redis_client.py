import os
from dotenv import load_dotenv
import redis
import numpy as np
import json

load_dotenv()

r = redis.Redis(
    host="localhost", port=6379, password=os.getenv("REDIS_PW"), decode_responses=False
)

REDIS_KEY_PREFIX = "fragentic:"


def get(key):
    key = REDIS_KEY_PREFIX + key
    result = r.get(key)
    if result is None:
        return None
    return result


def get_hashed(key):
    pass


def set(key, value):
    key = REDIS_KEY_PREFIX + key
    r.set(key, json.dumps(value))


def set_hashed(key):
    pass
