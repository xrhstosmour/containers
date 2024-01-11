from os import getenv
from urllib.parse import quote_plus

# Default values for redbeat lock timeout and maximum interval.
# Redbeat lock timeout must be greater than redbeat maximum interval.
# Links for help: https://github.com/sibson/redbeat/issues/129 & https://github.com/sibson/redbeat/issues/92.
DEFAULT_REDBEAT_LOCK_TIMEOUT = 1500
DEFAULT_REDBEAT_MAXIMUM_INTERVAL = 300

# Redbeat lock timeout and maximum interval configuration.
REDBEAT_LOCK_TIMEOUT: int = int(
    getenv("REDBEAT_LOCK_TIMEOUT", DEFAULT_REDBEAT_LOCK_TIMEOUT)
)
REDBEAT_MAXIMUM_INTERVAL: int = int(
    getenv("REDBEAT_MAXIMUM_INTERVAL", DEFAULT_REDBEAT_MAXIMUM_INTERVAL)
)
REDBEAT_LOCK_KEY: str = getenv("REDBEAT_LOCK_KEY", "redbeat:lock")

# Redis connection string.
REDIS_CONNECTION_STRING: str = f"redis://:{quote_plus(getenv('REDIS_PASSWORD'), safe='')}@{getenv('REDIS_HOST')}:{getenv('REDIS_PORT')}/{getenv('REDIS_DATABASE')}"

# RabbitMQ connection string.
RABBITMQ_CONNECTION_STRING: str = f"amqp://{getenv('RABBITMQ_USER')}:{quote_plus(getenv('RABBITMQ_PASSWORD'), safe='')}@{getenv('RABBITMQ_HOST')}:{getenv('RABBITMQ_PORT')}/"
