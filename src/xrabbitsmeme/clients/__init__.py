from asyncio import Queue

import httpx
from httpx import AsyncClient


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseClient:
    client: AsyncClient
    max_connection: float = 60.0
    queue: Queue

    def __init__(self):
        self.queue = Queue(maxsize=int(self.max_connection))
        timeout = httpx.Timeout(10.0, connect=self.max_connection)
        self.client = httpx.AsyncClient(timeout=timeout)

    async def close(self):
        await self.client.aclose()

