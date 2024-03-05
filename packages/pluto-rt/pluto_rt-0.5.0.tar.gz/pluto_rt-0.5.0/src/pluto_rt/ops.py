import pickle

from django.conf import settings
from django_redis import get_redis_connection


class Queue:
    """A simple implementation of message queuing in redis.
    We can't push python data structures directly into redis -
    must pickle to push and unpickle to retrieve.
    """

    QUEUE_EXHAUSTED = '"_queue_exhausted_"'

    def __init__(self, name, **kwargs):
        self.name = name
        self.redis = get_redis_connection("default")

    def complete(self):
        self.push(self.QUEUE_EXHAUSTED)

    def push(self, message):
        message = pickle.dumps(message)
        self.redis.lpush(self.name, message)

    def pop(self):
        raw_message = self.redis.rpop(self.name)
        if raw_message:
            message = pickle.loads(raw_message)
            return message

        return None


def get_rt_queue_handle(queue_name: str) -> Queue:
    """Get a handle on a redis message queueing connection, for reading or writing.

    Queue name should include a function descriptor and ID like "equipment_upload_357"
    """
    prefix = settings.CACHES["default"].get("KEY_PREFIX", "default")
    return Queue(f"{prefix}_{queue_name}")
