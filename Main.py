import time
import ac3
from HidatoGenerator import *
from HidatoCSP import *
from SolverCSP import *
import sys

DIM = 5


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


@timeit
def solve_hidato(width, height):
    print(f'Solving a {width} x {height} Hidato...\n')

    gen = HidatoGenerator()
    hidato = gen.generateHidato(width, height, alpha=0.5)
    print("Before solve:")
    hidato.display()

    sys.stdout.flush()

    arcs = [(i, i+1) for i in hidato.get_variables() if i < hidato.size]
    arcs.extend((i, i - 1) for i in hidato.get_variables() if i > 1)
    result = ac3.ac3(hidato, arcs)
    result = ac3.ac3(hidato, arcs)

    print("\nAfter solve:")
    _solve(hidato)
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
