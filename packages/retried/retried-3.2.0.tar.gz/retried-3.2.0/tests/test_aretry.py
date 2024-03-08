import asyncio
from random import random
from sys import maxsize

from retried import aretry
from retried import exponential_backoff


def func(a, b, c):
    if random() < 0.5:  # noqa: S311
        1 / 0  # type: ignore[reportUnusedExpression]


async def afunc(*args, **kwargs):
    return func(*args, **kwargs)


def test_exponential_backoff():
    b = exponential_backoff(1)
    assert next(b) == 0
    assert next(b) == 1
    assert next(b) == 2
    assert next(b) == 4
    assert next(b) == 8
    assert next(b) == 16
    assert next(b) == 32


def test_retry():
    aretry(maxsize)(func)(1, 2, c=3)
    asyncio.run(aretry(maxsize)(afunc)(1, 2, c=3))
