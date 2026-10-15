from abc import ABC, abstractmethod

class CacheService(ABC):
    @abstractmethod
    async def get(self, key):
        pass
    @abstractmethod
    async def set(self, key, value, timeout=None):
        pass
    @abstractmethod
    async def delete(self, key):
        pass
