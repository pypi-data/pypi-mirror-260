import asyncio
from functools import wraps
from itertools import count
import logging
import time
import typing as t


logger = logging.getLogger(__name__)


FACTOR = 0.0001


def exponential_backoff(factor: float) -> t.Iterator[float]:
    # https://github.com/encode/httpcore/blob/0211d10218acf97af46a134679203849d4489b13/httpcore/_async/connection.py#L23C1-L23C1
    yield 0
    # https://docs.python.org/3/library/itertools.html#itertools.count
    for n in count():
        yield factor * 2**n


def aretry(retries: int = 0):
    def decorator(f):
        @wraps(f)
        async def awrapper(*args, **kwargs):
            # https://github.com/encode/httpcore/blob/0211d10218acf97af46a134679203849d4489b13/httpcore/_async/connection.py#L98
            retries_left = retries
            delays = exponential_backoff(factor=FACTOR)
            while True:
                try:
                    rv = await f(*args, **kwargs)
                except ZeroDivisionError as e:
                    if retries_left <= 0:
                        raise Exception(f"fail with {retries = }") from e  # noqa: TRY002
                    retries_left -= 1
                    delay = next(delays)
                    logger.warning(f"{delay = } seconds ... {args=} {kwargs=} {f=}")
                    await asyncio.sleep(delay)
                else:
                    return rv

        if asyncio.iscoroutinefunction(f):
            return awrapper

        @wraps(f)
        def wrapper(*args, **kwargs):
            # https://github.com/encode/httpcore/blob/0211d10218acf97af46a134679203849d4489b13/httpcore/_async/connection.py#L98
            retries_left = retries
            delays = exponential_backoff(factor=FACTOR)
            while True:
                try:
                    rv = f(*args, **kwargs)
                except ZeroDivisionError as e:
                    if retries_left <= 0:
                        raise Exception(f"fail with {retries = }") from e  # noqa: TRY002
                    retries_left -= 1
                    delay = next(delays)
                    logger.warning(f"{delay = } seconds ... {args=} {kwargs=} {f=}")
                    time.sleep(delay)
                else:
                    return rv

        return wrapper

    return decorator
