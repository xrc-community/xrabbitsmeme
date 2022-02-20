from fastapi import APIRouter

from xrabbitsmeme.models.resource import Resource

router = APIRouter()


@router.get('/resources/me')
async def my_resources():
    resource = await Resource.get_or_404(1)
    return resource.to_dict()


def init_app(app):
    app.include_router(router)
