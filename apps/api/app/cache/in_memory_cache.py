import time


class InMemoryCache:
    def __init__(self):
        self.cache = {}

    def set(self, key, value, ttl=None):
        expiration_time = time.time() + ttl if ttl else None
        self.cache[key] = (value, expiration_time)

    def get(self, key):
        if key in self.cache:
            value, expiration_time = self.cache[key]
            if expiration_time is None or time.time() < expiration_time:
                return value
            else:
                del self.cache[key]  # Remove expired entry
        return None

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        self.cache.clear()
