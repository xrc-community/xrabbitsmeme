import logging
import os

from fastapi import FastAPI
from importlib.metadata import entry_points
from starlette.staticfiles import StaticFiles

from .db import db

logger = logging.getLogger(__name__)


def load_modules(app=None):
    for ep in entry_points()['xrabbitsmeme.modules']:
        logger.info("Loading module: %s", ep.name)
        init_app = ep.load()
        if app and init_app:
            init_app(app)


def get_app():
    app = FastAPI(title='X Rabbits Club Meme')
    if not os.path.exists(f'static'):
        os.makedirs(f'static')
    app.mount('/static', StaticFiles(directory='static'), name='static')
    db.init_app(app)
    load_modules(app)
    return app
