import argparse
import random
import sys

from board_generator import HidatoGenerator
from csp_solver import CSPSolver
from utils import timeit
from hidato_csp import HidatoCSP
from hidato_search_problem import HidatoSearchProblem
from HillClimber import HillClimber

DEFAULT_ALPHA = 0.5
DEFAULT_DIMENSION = 14


@timeit
def generate_hidato(width, height, alpha):
    print(f'Solving a {width} x {height} Hidato...\n')
    grid = _generate_hidato_grid(height, width, alpha)
    print(grid)
    return grid

    # hidato = gen.generate_hidato_csp(width, height, alpha=0.5)
    # print("Before solve:")
    # hidato.display()
    #
    # sys.stdout.flush()
    #
    # return hidato


def _generate_hidato_grid(height, width, alpha):
    gen = HidatoGenerator()
    grid = gen.generate_grid(width, height, alpha)
    return grid


@timeit
def _solve_csp(width, height, grid, select_variable, order_values, forward_checking):
    hidato = HidatoCSP(width, height, grid)
    solver = CSPSolver(hidato)
    solver.solve(select_variable, order_values, forward_checking)
    hidato.display()

    print(f"Solution is {'correct' if hidato.is_correct() else 'incorrect'}.")


def benchmark(width, height, grid):
    hidato = HidatoCSP(width, height, grid)

    time_with_fc = _solve_csp(hidato, select_variable="MRV", order_values="LCV", forward_checking=True)
    time_without_fc = _solve_csp(hidato, select_variable="MRV", order_values="LCV", forward_checking=False)


def _solve_hill_climbing(width, height, grid):
    problem = HidatoSearchProblem(5, 5, grid)
    solver = HillClimber()
    solver.solve(problem)


def main():
    parser = argparse.ArgumentParser(description='Hidato Solver')
    parser.add_argument('--hill', dest='hill_climbing', action='store_true')
    parser.add_argument('--benchmark', dest='benchmark', action='store_true')
    parser.add_argument('--dim', dest="dimension", default=DEFAULT_DIMENSION, type=int)
    parser.add_argument('--a', dest="alpha", default=DEFAULT_ALPHA, type=float)

    args = parser.parse_args()

    width = height = args.dimension
    grid = generate_hidato(width, height, args.alpha)

    if args.benchmark:
        benchmark(width, height, grid)
    if args.hill_climbing:
        _solve_hill_climbing(width, height, grid)
    else:
        _solve_csp(width, height, grid, select_variable="MRV", order_values="LCV", forward_checking=False)

    print("\nAfter solve:")



if __name__ == '__main__':
    main()
