import time

from HidatoGenerator import *
from HidatoCSP import *
from SolverCSP import *


def is_consistent(width, height, grid):
    val = grid.index(1)
    x_before = val // width
    y_before = val % width
    flag = True
    for i in range(2, width * height + 1):
        val = grid.index(i)
        x, y = val // width, val % width
        if abs(x_before - x) > 1 or abs(y_before - y) > 1:
            flag = False
            break
        else:
            if flag:
                x_before = x
                y_before = y
    return flag


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
