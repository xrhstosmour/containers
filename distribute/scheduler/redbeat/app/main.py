from os import getenv

from app.configuration import (
    DEFAULT_REDBEAT_LOCK_TIMEOUT,
    DEFAULT_REDBEAT_MAXIMUM_INTERVAL,
    RABBITMQ_CONNECTION_STRING,
    REDBEAT_LOCK_KEY,
    REDBEAT_LOCK_TIMEOUT,
    REDBEAT_MAXIMUM_INTERVAL,
    REDIS_CONNECTION_STRING,
)
from app.redis import delete_redis_lock
from celery import Celery

# Delete redis data used for locking mechanism.
delete_redis_lock(lock_name=REDBEAT_LOCK_KEY)

# Check if REDBEAT_LOCK_TIMEOUT is greater than REDBEAT_MAXIMUM_INTERVAL.
set_default_values: bool = False
if REDBEAT_LOCK_TIMEOUT <= REDBEAT_MAXIMUM_INTERVAL:
    print(
        "WARNING: REDBEAT_LOCK_TIMEOUT should be greater than"
        " REDBEAT_MAXIMUM_INTERVAL! Default values will be used!"
    )
    set_default_values = True

# Celery worker instance.
celery_worker: Celery = Celery(
    "worker",
    broker=RABBITMQ_CONNECTION_STRING,
    backend=REDIS_CONNECTION_STRING,
    redbeat_redis_url=REDIS_CONNECTION_STRING,
    redbeat_lock_key=getenv("REDBEAT_LOCK_KEY"),
)

# Celery worker configuration.
celery_worker.conf.update(
    worker_prefetch_multiplier=1,
    broker_heartbeat=0,
    task_acks_late=True,
    timezone="UTC",
    worker_max_tasks_per_child=1,
    REDBEAT_LOCK_TIMEOUT=(
        DEFAULT_REDBEAT_LOCK_TIMEOUT
        if set_default_values
        else REDBEAT_LOCK_TIMEOUT
    ),
    beat_max_loop_interval=(
        DEFAULT_REDBEAT_MAXIMUM_INTERVAL
        if set_default_values
        else REDBEAT_MAXIMUM_INTERVAL
    ),
)
