from datetime import timedelta
from functools import partial
from functools import wraps
from itertools import cycle
from itertools import repeat
import logging
import time
import typing as t


logger = logging.getLogger(__name__)


T = t.TypeVar('T')
SingleOrTuple = t.Union[t.Type[T], tuple[t.Type[T], ...]]

DelayT = t.Union[timedelta, float]
DelaysT = t.Iterator[DelayT]
RetriesT = t.Optional[int]


def delay_to_sec(delay: DelayT):
    if isinstance(delay, timedelta):
        delay = delay.total_seconds()
    return delay


def default_error_callback(index: int, exception: Exception, delay: DelayT, retries: RetriesT):
    log_prefix = f'try {index} of {retries} -> {exception!r}'
    is_last = index == retries
    if not is_last:
        logger.info(f'{log_prefix} -> sleep {delay_to_sec(delay)} seconds')
    else:
        logger.warning(log_prefix)


def retry(
    retries: RetriesT = None,
    *,
    exceptions: SingleOrTuple[Exception] = Exception,
    error_callback: t.Callable[[int, Exception, DelayT, RetriesT], None] = default_error_callback,
    sleeper: t.Callable[[float], None] = time.sleep,
    delays: DelaysT = repeat(0),
    first_delay: t.Optional[DelayT] = None,
    chain_exception: bool = True,
):

    delays = cycle(delays)
    if first_delay is None:
        first_delay = next(delays)

    def callback(index: int, exception: Exception, delay: DelayT, retries: RetriesT):
        error_callback(index, exception, delay, retries)
        sleeper(delay_to_sec(delay))

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            function_retrying = partial(f, *args, **kwargs)
            try:
                # execute once
                return function_retrying()
            except exceptions as e:
                # start retrying
                i = 0
                callback(i, e, first_delay, retries)
                # retrying
                while True:
                    try:
                        return function_retrying()
                    except exceptions as e:
                        # check first
                        if i == retries:
                            if chain_exception:
                                raise
                            raise e from None
                        # then ++
                        i += 1
                        delay = next(delays)
                        callback(i, e, delay, retries)

        return wrapper

    return decorator


if __name__ == '__main__':
    from random import random

    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-7s %(message)s')

    class Error(Exception):
        pass

    @retry(
        retries=2,
        exceptions=(ValueError, ZeroDivisionError, Error),
        # error_callback=lambda i, e, d, r: print(i),
        delays=cycle([1 / 3, 2 / 3]),
        first_delay=1.5,
    )
    def f():
        1 / 0  # type: ignore[reportUnusedExpression]

        if random() < 0.2:
            return

        if random() < 0.8:
            # return
            1 / 0  # type: ignore[reportUnusedExpression]
        if random() < 0.8:
            raise Error('??')

    f()
