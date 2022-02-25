from functools import wraps

import asyncio
import typer

from xrabbitsmeme import config
from xrabbitsmeme.main import db


app = typer.Typer()


def async_cmd(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def app_context():
    def wrapper(f):
        @wraps(f)
        async def wrapped(*args, **kwargs):
            await db.set_bind(config.DB_DSN)
            await f(*args, **kwargs)

        return wrapped

    return wrapper
