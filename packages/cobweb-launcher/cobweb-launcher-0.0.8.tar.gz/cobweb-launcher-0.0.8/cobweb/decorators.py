from functools import wraps
from cobweb import log


def check_redis_status(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            log.exception(e)

    return wrapper

