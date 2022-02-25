import os
from typing import List

import aiofiles
from fastapi import APIRouter, UploadFile, Form
from pydantic import BaseModel
from starlette.requests import Request

from ..db import db
from ..utils.utils import generate_image_url
from .models import Material

router = APIRouter()


class MaterialModel(BaseModel):
    category: str
    name: str


@router.post('/materials')
async def create_material(file: UploadFile, category: str = Form(...), name: str = Form(...)):
    async with db.transaction():
        material = await Material.create(category=category, name=name)
        filename = f'{material.id}.png'
        dir_path = f'static/materials/{category}'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        async with aiofiles.open(f'{dir_path}/{filename}', 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        await material.update(filename=filename).apply()
        return dict(success=True)


@router.get('/materials')
async def material_list(request: Request):
    materials: List[Material] = await Material.query.gino.all()
    results = []
    for material in materials:
        image_url = generate_image_url(request, f'/static/materials/{material.category}/{material.filename}')
        ret = material.to_dict()
        ret.update(dict(image_url=image_url))
        results.append(ret)
    return results


def init_app(app):
    app.include_router(router)
