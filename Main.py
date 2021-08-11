import time

from HidatoGenerator import *
from HidatoCSP import *
from SolverCSP import *
import sys


def is_consistent(hidato):
    index = hidato.grid.index(1)
    x_before = index // hidato.width
    y_before = index % hidato.width
    for i in range(2, hidato.width * hidato.height + 1):
        index = hidato.grid.index(i)
        x, y = index // hidato.width, index % hidato.width
        if abs(x_before - x) > 1 or abs(y_before - y) > 1:
            return False
        x_before = x
        y_before = y
    return True


DIM = 15


def timeit(func):
    def timed_func(*args, **kwargs):
        start = time.time()
        func(*args, *kwargs)
        end = time.time() - start
        print(f'Running {func.__name__} took ' + '{0:.4g}'.format(end) + ' seconds.')
    return timed_func

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

    correct = is_consistent(hidato)
    print(f"Solution is {'correct' if correct else 'incorrect'}.")

@timeit
def _solve(hidato):
    solver = SolverCSP()
    solver.solve(hidato)

def main():
    random.seed(0)
    width = height = 10
    solve_hidato(width, height)


if __name__ == '__main__':
    main()
