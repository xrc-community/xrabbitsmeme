from .app import cron_jobs, queue_tasks, redis_settings, shutdown, startup
from ..nfts import tasks


class WorkerSettings:
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = redis_settings
    cron_jobs = cron_jobs
    functions = queue_tasks
