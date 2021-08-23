import argparse
import itertools
import sys
import time
from collections import defaultdict

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from board_generator import HidatoGenerator
from csp_solver import CSPSolver
from hidato_csp import HidatoCSP
from hidato_search_problem import HidatoSearchProblem
from hill_climber import HillClimber
from utils import timeit, _time_since

DEFAULT_ALPHA = 0.5
DEFAULT_DIMENSION = 5
BENCHMARK_ITERATIONS = 10


def generate_hidato(width, height, alpha):
    gen = HidatoGenerator()
    return gen.generate_grid(width, height, alpha)


def _solve_csp(width, height, grid, select_variable, order_values, forward_checking, display=True):
    problem = HidatoCSP(width, height, grid)
    if display:
        problem.display()

    solver = CSPSolver(problem)
    solver.solve(select_variable, order_values, forward_checking)
    return problem, solver._num_of_iterations


def _solve_hill_climbing(width, height, grid):
    problem = HidatoSearchProblem(width, height, grid)
    problem.display()
    solver = HillClimber()
    solver.solve(problem)
    return problem


def benchmark(width, height, alpha):
    select_variables_options = ["Ordered", "MRV"]
    order_values_options = ["Random", "LCV"]
    forward_checking = [True, False]


    results = []
    for i in range(BENCHMARK_ITERATIONS):
        grid = generate_hidato(width, height, alpha)

        for select_var, order_values, fc in itertools.product(select_variables_options, order_values_options,
                                                              forward_checking):
            start = time.time()
            _, num_of_backtracking = _solve_csp(width, height, grid, select_var, order_values, fc, False)
            time_since = _time_since(start)

            results.append((select_var, order_values, fc, i, time_since, num_of_backtracking))

    plot_results(results)

def plot_results(results):
    df = pd.DataFrame(results, columns=["select_var", "order_values", "fc", "iteration", "time"])
    df.to_csv('csp_runtimes.csv')
    print(df)


def main():
    args = parse_args()

    width = height = args.dimension

    if args.benchmark:
        benchmark(width, height, args.alpha)
        return

    print(f'Solving a {width} x {height} Hidato...\n')
    grid = generate_hidato(width, height, args.alpha)

    if args.hill_climbing:
        problem, _ = _solve_hill_climbing(width, height, grid)
    elif args.csp:
        problem, _ = _solve_csp(width, height, grid, select_variable="MRV", order_values="LCV", forward_checking=False)

    print("\nAfter solve:")
    sys.stdout.flush()
    problem.display()
    is_correct = problem.is_correct()
    print(f"Solution is {'correct' if is_correct else 'incorrect'}.")
    if not is_correct:
        loss = problem.get_loss(problem.grid)
        print(f"There are {loss} errors.")


def parse_args():
    parser = setup_arg_parser()
    args = parser.parse_args()
    return args


def setup_arg_parser():
    parser = argparse.ArgumentParser(description='Hidato Solver')
    parser.add_argument('--csp', dest='csp', default=True, action='store_true')
    parser.add_argument('--hill', dest='hill_climbing', action='store_true')
    parser.add_argument('--benchmark', dest='benchmark', action='store_true')
    parser.add_argument('--dim', dest="dimension", default=DEFAULT_DIMENSION, type=int)
    parser.add_argument('--a', dest="alpha", default=DEFAULT_ALPHA, type=float)
    return parser


if __name__ == '__main__':
    main()
