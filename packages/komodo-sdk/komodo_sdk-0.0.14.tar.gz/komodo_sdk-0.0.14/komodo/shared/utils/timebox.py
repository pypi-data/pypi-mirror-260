import signal
import time
from contextlib import contextmanager
from functools import wraps
from textwrap import shorten


class TimeoutException(Exception): pass


def time_print(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print_args = [arg_class_or_value(arg) for arg in args]
        print(f'Function {func.__name__}{print_args} {kwargs} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


def time_print_simple(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


def arg_class_or_value(arg):
    if ('aplus' in str(type(arg))):
        return arg.__class__.__name__
    return shorten(arg, 24, placeholder="...") if isinstance(arg, str) else arg


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    try:
        with time_limit(3):
            time.sleep(5)
            print('Done')
    except TimeoutException:
        print("Timed out!")
