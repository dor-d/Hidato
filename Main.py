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
        end = time.time() - start
        print(f'Running {func.__name__} took ' + '{0:.4g}'.format(end) + ' seconds.')
    return timed_func

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
    # width = height = DIM
    solve_hidato(6, 5)


if __name__ == '__main__':
    main()
