import collections
import sys
import numpy as np
from bson import ObjectId


class LRUCache:
    def __init__(self, initial_data=None, max_size_bytes=100 * 1024 * 1024):
        """
        initial_data: optional dict of {key: value} to pre-fill the cache
        """
        self.cache = collections.OrderedDict()
        self.max_size = max_size_bytes
        self.current_size = 0
        self.doc_size = 20000

        if initial_data:
            for k, v in initial_data.items():
                # Convert embedding lists to numpy arrays
                if isinstance(v.get("embedding"), list):
                    v["embedding"] = np.array(v["embedding"])
                # Convert string _id back to ObjectId
                if "_id" in v and isinstance(v["_id"], str):
                    v["_id"] = ObjectId(v["_id"])
                self.put(k, v)

    def get(self, key):
        if key not in self.cache:
            return None
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def put(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
            self.current_size -= self.doc_size

        self.cache[key] = value
        self.current_size += self.doc_size

        # Evict least recently used items if over size
        while self.current_size > self.max_size:
            self.cache.popitem(last=False)
            self.current_size -= self.doc_size

    def __contains__(self, key):
        return key in self.cache

    def __len__(self):
        return len(self.cache)

    def to_dict(self):
        """Return a JSON-serializable version of the cache."""
        result = {}
        for k, v in self.cache.items():
            new_val = v.copy()
            # Convert embedding to list if it's a numpy array
            if isinstance(new_val.get("embedding"), np.ndarray):
                new_val["embedding"] = new_val["embedding"].tolist()
            # Convert ObjectId to string if present
            if "_id" in new_val:
                new_val["_id"] = str(new_val["_id"])
            result[k] = new_val
        return result
