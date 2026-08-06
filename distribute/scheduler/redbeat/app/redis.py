import logging
from urllib.parse import urlparse

from app.configuration import REDIS_CONNECTION_STRING
from redis import ConnectionError, Redis, RedisError


def create_redis_client() -> Redis:
    """Create a Redis client instance.

    Returns:
        Redis: The Redis client instance.
    """
    # Get the needed information from the connection string.
    url = urlparse(REDIS_CONNECTION_STRING)

    # Create and the Redis connection.
    return Redis(
        host=url.hostname,
        port=url.port,
        db=int(url.path.lstrip("/")),
        password=url.password,
    )


def delete_redis_lock(lock_name: str) -> None:
    """Delete redis lock, via its name, but only if it is actually stale.

    RedBeat always acquires its lock with an explicit TTL, so a lock held
    by a live (or freshly crashed) process always reports a positive TTL,
    and Redis itself removes the key once that TTL expires. A lock is
    only genuinely stuck if it exists without a TTL at all (ttl == -1),
    which should not happen under normal RedBeat operation. Deleting the
    lock whenever it merely exists would force-remove a lock a still
    running beat process legitimately owns, defeating RedBeat's
    single-scheduler guarantee during rolling restarts.

    Args:
        lock_name (str): The name of the lock.
    """
    try:
        time_to_live: int = redis_client.ttl(lock_name)
        # -2 means the key does not exist, nothing to delete.
        # -1 means the key exists without an expiry, which is stale.
        if time_to_live == -1:
            logging.info(f"Deleting stale lock: {lock_name}...")
            redis_client.delete(lock_name)
    except ConnectionError as connection_error:
        logging.error(connection_error)
    except RedisError as redis_error:
        logging.error(redis_error)


# Redis client instance.
redis_client: Redis = create_redis_client()
