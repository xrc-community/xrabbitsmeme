from fastapi import Query
from starlette.requests import Request

from .gino_starlette import Gino
from . import config

db = Gino(
    dsn=config.DB_DSN,
    pool_min_size=config.DB_POOL_MIN_SIZE,
    pool_max_size=config.DB_POOL_MAX_SIZE,
    echo=config.DB_ECHO,
    ssl=config.DB_SSL,
    use_connection_for_request=config.DB_USE_CONNECTION_FOR_REQUEST,
    retry_limit=config.DB_RETRY_LIMIT,
    retry_interval=config.DB_RETRY_INTERVAL,
)


class Pagination:
    default_per_page = 10

    def __init__(
        self, request: Request, per_page: int = Query(default=default_per_page, ge=1),
    ):
        self.request = request
        self.per_page = per_page

    async def paginate(
        self, query, loader=None, dump_func=None, async_dump_func=None
    ) -> dict:
        if loader:
            query = query.execution_options(loader=loader)
        rows = []
        ids = []
        async with db.transaction():
            cursor = await db.iterate(query)
            while len(rows) < self.per_page:
                ret = await cursor.many(self.per_page)
                if len(ret) == 0:
                    break
                for row in ret:
                    if row.id not in ids:
                        rows.append(row)
                        ids.append(row.id)
            rows = rows[: self.per_page]
        has_next = self.per_page == len(rows)
        if async_dump_func:
            data = [await async_dump_func(row) for row in rows]
        elif dump_func:
            data = [dump_func(row) for row in rows]
        else:
            data = [row.to_dict() for row in rows]
        return dict(
            pagination=dict(page=1, per_page=self.per_page, has_next=has_next),
            rows=data,
        )