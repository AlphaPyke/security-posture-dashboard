from redis import Redis
from rq import Queue

from app.core.config import settings

SCAN_QUEUE_NAME = "scorecard-scans"


def get_scan_queue() -> Queue:
    return Queue(SCAN_QUEUE_NAME, connection=Redis.from_url(settings.redis_url))


def enqueue_scan(scan_id: int) -> None:
    queue = get_scan_queue()
    queue.enqueue("app.workers.scorecard.run_scan_job", scan_id)
