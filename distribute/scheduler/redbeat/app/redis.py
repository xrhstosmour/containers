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
    """Delete redis lock, via its name.

    Args:
        lock_name (str): The name of the lock.
    """
    try:
        # Delete the lock if it exists.
        if redis_client.exists(lock_name):
            logging.info(f"Deleting lock: {lock_name}...")
            redis_client.delete(lock_name)
    except ConnectionError as connection_error:
        logging.error(connection_error)
    except RedisError as redis_error:
        logging.error(redis_error)


# Redis client instance.
redis_client: Redis = create_redis_client()
