import os
import uuid
from typing import List

from httpx import Response

from ..clients import Singleton, BaseClient


class IPFSClient(BaseClient, metaclass=Singleton):
    base_url: str = 'https://ipfs.io/ipfs'
    support_schemas: List[str] = ['https://', 'http://', 'ipfs://']

    async def get(self, path: str) -> Response:
        if not path.startswith('/'):
            path = '/' + path
        await self.queue.put(1)
        resp = await self.client.get(f'{self.base_url}{path}')
        if not self.queue.empty():
            await self.queue.get()
        return resp

    async def download(self, path: str, image_url: str, filename: str = None) -> str:
        image_url = self.generate_image_url(image_url)
        local_filename = filename or f'{uuid.uuid4()}.png'
        if not os.path.exists(f'static/{path}'):
            os.makedirs(f'static/{path}')
        await self.queue.put(1)
        async with self.client.stream('GET', image_url) as response:
            with open(f'static/{path}/{local_filename}', 'wb') as f:
                async for chunk in response.aiter_bytes():
                    f.write(chunk)
        if not self.queue.empty():
            await self.queue.get()
        return local_filename

    @classmethod
    def generate_image_url(cls, image_url: str) -> str:
        support = False
        for schema in cls.support_schemas:
            if image_url.startswith(schema):
                support = True
                break
        if not support:
            return ''
        if image_url.startswith('ipfs://'):
            image_url = f'{cls.base_url}/{image_url[7:]}'
        return image_url

    @classmethod
    def generate_info_url(cls, ipfs_path: str) -> str:
        return f'{cls.base_url}/{ipfs_path}'
