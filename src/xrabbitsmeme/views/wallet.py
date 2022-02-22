from fastapi import APIRouter

from xrabbitsmeme.models.wallet import Wallet

router = APIRouter()


@router.get('/wallets/info')
async def my_wallet_info():
    wallet = await Wallet.get_or_404(1)
    return wallet.to_dict()


def init_app(app):
    app.include_router(router)