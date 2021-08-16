import argparse
import random
import sys

from board_generator import HidatoGenerator
from csp_solver import CSPSolver
from utils import timeit

DEFAULT_DIMENSION = 14


@timeit
def generate_hidato(width, height):
    # For debug purpose
    random.seed(0)

    print(f'Solving a {width} x {height} Hidato...\n')

    gen = HidatoGenerator()
    hidato = gen.generate_hidato(width, height, alpha=0.5)
    print("Before solve:")
    hidato.display()

    sys.stdout.flush()

    return hidato


@timeit
def _solve(hidato, select_variable, order_values, forward_checking):
    print("\nAfter solve:")

    solver = CSPSolver(hidato)
    solver.solve(select_variable, order_values, forward_checking)
    hidato.display()

    print(f"Solution is {'correct' if hidato.is_correct() else 'incorrect'}.")


def solve_hidato(dimension):
    width = height = dimension
    hidato = generate_hidato(width, height)
    _solve(hidato, select_variable="MRV", order_values="LCV", forward_checking=True)


def benchmark():
    width = height = DEFAULT_DIMENSION
    hidato = generate_hidato(width, height)
    time_with_fc = _solve(hidato, select_variable="MRV", order_values="LCV", forward_checking=True)
    time_without_fc = _solve(hidato, select_variable="MRV", order_values="LCV", forward_checking=False)


def main():
    parser = argparse.ArgumentParser(description='Hidato Solver')
    parser.add_argument('--benchmark', dest='benchmark', action='store_true')
    parser.add_argument('--dim', dest="dimension", default=DEFAULT_DIMENSION, type=int)
    args = parser.parse_args()

    if args.benchmark:
        benchmark()
    else:
        solve_hidato(args.dimension)


if __name__ == '__main__':
    main()
