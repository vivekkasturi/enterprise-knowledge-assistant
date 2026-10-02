class CacheService:
    def __init__(self, cache):
        self.cache = cache

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value, timeout=None):
        self.cache.set(key, value, timeout)

    def delete(self, key):
        self.cache.delete(key)