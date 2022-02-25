import json
from typing import List

from xrabbitsmeme.clients.ipfs import IPFSClient
from xrabbitsmeme.nfts.models import NFT, NFTSeries
from xrabbitsmeme.cli.app import app, async_cmd, app_context


async def _update_nft_info(nft: NFT, ipfs_path: str) -> NFT:
    client = IPFSClient()
    resp = await client.get(f'/{ipfs_path}/{nft.no}')
    if resp.status_code == 200:
        data = resp.json()
        await nft.update(info=json.dumps(data)).apply()
        return nft


async def _update_nft_filename(nft: NFT, ipfs_path: str, info: dict):
    client = IPFSClient()
    image_url = info.get('image', '')
    if image_url:
        filename = await client.download(ipfs_path, image_url, f'{nft.no}.png')
        await nft.update(filename=filename).apply()


@app.command()
@async_cmd
@app_context()
async def create_nfts(ipfs_path: str):
    series: NFTSeries = await NFTSeries.query.where(NFTSeries.ipfs_path == ipfs_path).gino.first()
    if not series:
        print('no series')
        return
    nfts = await NFT.query.where(NFT.series_id == series.id).order_by(NFT.no).gino.all()
    failed_info_no: List[int] = []
    failed_image_no: List[int] = []
    for nft in nfts:
        if not nft.info:
            try:
                nft = await _update_nft_info(nft, ipfs_path)
                print(f'Updated nft info {nft.no}')
            except Exception as e:
                failed_info_no.append(nft.no)
                print(f'error fetch info for {nft.no}. error: {e}')
        if not nft.filename:
            info = nft.info
            if not info:
                continue
            info = json.loads(nft.info)
            try:
                await _update_nft_filename(nft, ipfs_path, info)
                print(f'Updated nft filename {nft.no}')
            except Exception as e:
                failed_image_no.append(nft.filename)
                print(f'error download image for {nft.no}-{info.get("image", "no image path")}. error: {e}')
    print('Failed fetch info count', len(failed_info_no))
    print('Failed download image count', len(failed_image_no))
    print('Failed fetch info no:', failed_info_no)
    print('Failed download image no:', failed_image_no)


if __name__ == '__main__':
    app()
