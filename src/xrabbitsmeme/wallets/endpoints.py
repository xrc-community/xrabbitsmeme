from fastapi import APIRouter

router = APIRouter()

@router.get('/wallets/info')
async def my_wallet_info():
    return dict(success=True)


def init_app(app):
    app.include_router(router)
