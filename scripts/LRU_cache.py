import collections
import sys
import numpy as np


class LRUCache:
    def __init__(self, initial_data=None, max_size_bytes=500 * 1024 * 1024):
        """
        initial_data: optional dict of {key: value} to pre-fill the cache
        """
        self.cache = collections.OrderedDict()
        self.max_size = max_size_bytes
        self.current_size = 0

        if initial_data:
            for k, v in initial_data.items():
                # Convert lists to numpy arrays for embeddings
                if isinstance(v, list):
                    v = np.array(v)
                self.put(k, v)

    def _estimate_size(self, value):
        """Estimate memory size of value (faster than deep introspection)."""
        if isinstance(value, np.ndarray):
            return value.nbytes
        elif isinstance(value, (list, tuple)):
            return sum(self._estimate_size(v) for v in value)
        elif isinstance(value, dict):
            return sum(
                self._estimate_size(k) + self._estimate_size(v)
                for k, v in value.items()
            )
        elif isinstance(value, str):
            return len(value.encode("utf-8"))
        elif isinstance(value, (int, float, bool)):
            return sys.getsizeof(value)
        else:
            return sys.getsizeof(value)

    def get(self, key):
        if key not in self.cache:
            print("Cache Miss")
            return None
        value = self.cache.pop(key)
        self.cache[key] = value
        print("Cache Hit")
        return value

    def put(self, key, value):
        if key in self.cache:
            old_value = self.cache.pop(key)
            self.current_size -= self._estimate_size(old_value)

        self.cache[key] = value
        self.current_size += self._estimate_size(value)

        # Evict least recently used items if over size
        while self.current_size > self.max_size:
            old_key, old_value = self.cache.popitem(last=False)
            self.current_size -= self._estimate_size(old_value)

    def __contains__(self, key):
        return key in self.cache

    def __len__(self):
        return len(self.cache)

    def to_dict(self):
        """Return a JSON-serializable version of the cache."""
        result = {}
        for k, v in self.cache.items():
            if isinstance(v, np.ndarray):
                result[k] = v.tolist()
            else:
                result[k] = v
        return result
