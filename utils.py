import time


def timeit(func):
    def timed_func(*args, **kwargs):
        start = time.time()
        func(*args, *kwargs)
        total = time.time() - start
        if total < 60:
            print(f'Running {func.__name__} took ' + '{0:.4g}'.format(total) + ' seconds.')
        else:
            mins = total // 60
            secs = total % 60
            print(
                f'Running {func.__name__} took {mins} minute{"s" if mins > 1 else ""} and {"{0:.4g}".format(secs)} seconds.')

    return timed_func