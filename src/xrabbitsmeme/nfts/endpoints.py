import json

# from arq import ArqRedis, create_pool
from typing import List

from fastapi import APIRouter, HTTPException, UploadFile, Form
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request

from ..clients.ipfs import IPFSClient
from ..db import db
from ..utils.utils import generate_image_url
# from ..worker import redis_settings
from .models import NFTSeries, NFT

router = APIRouter()


class NFTSeriesModel(BaseModel):
    ipfs_path: str
    name: str
    supply: int


@router.post('/series')
async def create_series(data: NFTSeriesModel):
    nft_series: NFTSeries = await NFTSeries.query.where(NFTSeries.ipfs_path == data.ipfs_path).gino.first()
    async with db.transaction():
        if not nft_series:
            nft_series = await NFTSeries.create(ipfs_path=data.ipfs_path, name=data.name, supply=data.supply)
        nfts: List[NFT] = await NFT.query.where(NFT.series_id == nft_series.id).gino.all()
        exist_nos = [nft.no for nft in nfts]
        create_nfts: List[dict] = []
        for no in range(nft_series.supply):
            if no not in exist_nos:
                create_nfts.append(dict(series_id=nft_series.id, no=no))
        if create_nfts:
            await NFT.insert().gino.all(create_nfts)
        return nft_series.to_dict()


@router.get('/series')
async def get_series():
    data = await NFTSeries.query.gino.all()
    return [item.to_dict() for item in data]


@router.get('/series/{path}')
async def get_series_by_path(path: str):
    series = await NFTSeries.query.where(NFTSeries.ipfs_path == path).gino.first()
    if not series:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'NFT Series not found')
    return series.to_dict()


@router.get('/series/{path}/nfts/{no}')
async def get_nft_by_no(path: str, no: int, request: Request):
    series: NFTSeries = await NFTSeries.query.where(NFTSeries.ipfs_path == path).gino.first()
    if not series:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'NFT Series not found')
    nft: NFT = await NFT.query.where(NFT.series_id == series.id).where(NFT.no == no).gino.first()
    if not nft:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'NFT not found')
    ret = nft.to_dict()
    image_url = ''
    filename = nft.filename
    info = nft.info
    if filename:
        image_url = generate_image_url(f'/static/{series.ipfs_path}/{filename}')
    if not image_url and info:
        image_url: str = info.get('image', '')
        image_url = IPFSClient.generate_image_url(image_url)
    ret.update(dict(
        image_url=image_url,
        info_url=IPFSClient.generate_info_url(f'{series.ipfs_path}/{nft.no}'),
    ))
    if info:
        ret.update(dict(info=json.loads(info)))
    return ret


def init_app(app):
    app.include_router(router)
