import json
import logging

from arq import ArqRedis

from ..clients.ipfs import IPFSClient
from ..worker.app import task
from .models import NFTSeries, NFT

log = logging.getLogger("arq.connections")


@task
async def generate_nft_series(ctx, series_id: int):
    redis: ArqRedis = ctx['redis']
    log.info(f'start generate nft for series {series_id}')
    nft_series = await NFTSeries.get(series_id)
    ipfs_path = nft_series.ipfs_path
    supply = nft_series.supply
    if not supply:
        return
    for no in range(supply):
        await redis.enqueue_job(
            'generate_nft', series_id, ipfs_path, no,
        )


@task
async def generate_nft(ctx, series_id: int, ipfs_path: str, no: int):
    redis: ArqRedis = ctx['redis']
    generate_key = f'generating_nfts_for_series_{series_id}_{no}'
    if await redis.get(generate_key):
        log.info(f'nft generating for series {series_id} no {no} is on progress')
        return
    image_url: str or None = None
    try:
        nft = await NFT.query.where(NFT.no == no).where(NFT.series_id == series_id).gino.first()
        if nft and nft.filename:
            await redis.delete(generate_key)
            return
        client = IPFSClient()
        if not nft:
            nft = await NFT.create(series_id=series_id, no=no)
        if not nft.info:
            resp = await client.get(f'/{ipfs_path}/{no}')
            if resp.status_code == 200:
                data = resp.json()
                nft.info = json.dumps(data)
                await nft.update(info=json.dumps(data)).apply()
        if nft.info:
            info = json.loads(nft.info)
            image_url = info.get('image', None)
            if image_url:
                filename = await client.download(ipfs_path, image_url, f'{no}.png')
                await nft.update(filename=filename).apply()
        else:
            raise Exception('fetch ipfs info failed')
        log.info(f'finish generate nft for series {series_id} no {no}')
    except Exception as e:
        log.info(f'error generate nft for series {series_id} no {no}, image_url: {image_url or "no image url"}. error: {e}')
        raise e
    finally:
        await redis.delete(generate_key)
