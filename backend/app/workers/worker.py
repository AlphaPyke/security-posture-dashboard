from redis import Redis
from rq import Worker

from app.core.config import settings
from app.services.queue import SCAN_QUEUE_NAME


def main() -> None:
    redis = Redis.from_url(settings.redis_url)
    Worker([SCAN_QUEUE_NAME], connection=redis).work()


if __name__ == "__main__":
    main()
