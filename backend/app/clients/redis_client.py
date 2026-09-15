import os
from dotenv import load_dotenv
import redis.asyncio as aioredis
import numpy as np
import json
from app.config import settings

load_dotenv()

r = aioredis.from_url(os.getenv("REDIS_URL"), decode_responses=False)

KEY_PREFIX = settings.redis.key_prefix


async def get(key):
    key = KEY_PREFIX + key
    result = await r.get(key)
    if result is None:
        return None
    return json.loads(result)


async def get_many_bytes(keys):
    return await r.mget([f"{KEY_PREFIX}{key}" for key in keys])


async def get_bytes(key):
    key = KEY_PREFIX + key
    result = await r.get(key)
    if result is None:
        return None
    return result


async def set(key, value):
    key = KEY_PREFIX + key
    return await r.set(key, json.dumps(value))


async def set_bytes(key, value):
    key = KEY_PREFIX + key
    return await r.set(key, value)


async def mset_bytes(mapping: dict):
    prefixed = {f"{KEY_PREFIX}{k}": v for k, v in mapping.items()}
    await r.mset(prefixed)
