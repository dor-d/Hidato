import time


def timeit(func):
    def timed_func(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        _print_runnning_time(_time_since(start), func.__name__)
        return result

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