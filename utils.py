import time
from collections import namedtuple
EMPTY = -1

Move = namedtuple('Move', ['x_pos', 'y_pos', 'number'])
Swap = namedtuple('Swap', ['x_1', 'y_1', 'x_2', 'y_2'])
Board = namedtuple('Board', ['grid'])

def timeit(func):
    def timed_func(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        time_since = _time_since(start)
        _print_runnning_time(time_since, func.__name__)
        return result, time_since

    return timed_func


def _time_since(start_time):
    return time.time() - start_time


def _print_runnning_time(runtime, function_name):
    if runtime < 60:
        print(f'Running {function_name} took {"{0:.4g}".format(runtime)} seconds.')
    else:
        mins = runtime // 60
        secs = runtime % 60
        print(
            f'Running {function_name} took {mins} minute{"s" if mins > 1 else ""} and {"{0:.4g}".format(secs)} seconds.')
