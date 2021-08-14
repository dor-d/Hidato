import time

from HidatoGenerator import *
from HidatoCSP import *
from SolverCSP import *
import sys

DIM = 14


def timeit(func):
    def timed_func(*args, **kwargs):
        start = time.time()
        func(*args, *kwargs)
        _print_runnning_time(_time_since(start), func.__name__)

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


@timeit
def solve_hidato(width, height):
    print(f'Solving a {width} x {height} Hidato...\n')

    gen = HidatoGenerator()
    hidato = gen.generateHidato(width, height, alpha=0.5)
    print("Before solve:")
    hidato.display()

    sys.stdout.flush()

    _solve(hidato)
    print("\nAfter solve:")
    hidato.display()

    print(f"Solution is {'correct' if hidato.is_correct() else 'incorrect'}.")


@timeit
def _solve(hidato):
    solver = SolverCSP()
    solver.solve(hidato)


def main():
    random.seed(0)
    width = height = DIM
    solve_hidato(width, height)


if __name__ == '__main__':
    main()
