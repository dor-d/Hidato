import time

from HidatoGenerator import *
from HidatoCSP import *
from SolverCSP import *

DIM = 15


def timeit(func):
    def timed_func():
        start = time.time()
        func()
        end = time.time() - start
        print(f'Running {func.__name__} took ' + '{0:.4g}'.format(end) + ' seconds.')
    return timed_func


# def solve_hidato

@timeit
def main():
    random.seed(0)

    width = height = 5
    gen = HidatoGenerator()
    hidato = gen.generateHidato(width, height, alpha=0.5)
    print("Before solve:")
    hidato.display()

    solver = SolverCSP()
    solver.solve(hidato)
    print("\nAfter solve:")
    hidato.display()


if __name__ == '__main__':
    main()
