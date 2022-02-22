import logging
from importlib.metadata import entry_points
from fastapi import FastAPI

from xrabbitsmeme.models import db

logger = logging.getLogger(__name__)


def load_modules(app=None):
    for ep in entry_points()['xrabbitsmeme.modules']:
        logger.info("Loading module: %s", ep.name)
        mod = ep.load()
        if app:
            init_app = getattr(mod, 'init_app', None)
            if init_app:
                init_app(app)


def get_app():
    app = FastAPI(title='X Rabbits Club Meme')
    db.init_app(app)
    load_modules(app)
    return app
