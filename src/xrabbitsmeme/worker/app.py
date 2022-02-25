import logging
from functools import wraps

from arq import cron, func
from arq.connections import RedisSettings

from ..clients.ipfs import IPFSClient
from ..db import db
from .. import config

log = logging.getLogger("arq.connections")
redis_settings = RedisSettings(
    host=config.REDIS_HOST, port=config.REDIS_PORT, database=config.REDIS_DB
)

cron_jobs = []
queue_tasks = []


def task(f):
    queue_tasks.append(func(f))

    @wraps(f)
    async def wrapper(*args, **kwargs):
        return await f(*args, **kwargs)

    return wrapper


def cron_task(**time_settings):
    def wrapper(f):
        cron_jobs.append(cron(f, **time_settings))

        @wraps(f)
        async def wrapped(*args, **kwargs):
            return await f(*args, **kwargs)

        return wrapped

    return wrapper


async def startup(ctx):
    await db.set_bind(config.DB_DSN)


async def shutdown(ctx):
    await IPFSClient().close()
    await db.pop_bind().close()
