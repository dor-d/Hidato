import argparse
import itertools
import sys
import time
import random

import numpy as np
import pandas as pd

from board_generator import HidatoGenerator
from csp_solver import CSPSolver
from hidato_csp import HidatoCSP
from hidato_search_problem import HidatoSearchProblem
from hill_climber import HillClimber
from utils import _time_since
from gui import HidatoUI

DEFAULT_ALPHA = 0.5
DEFAULT_DIMENSION = 5
BENCHMARK_ITERATIONS = 10
MICROSECS_IN_SECS = 1e6
THE_FUNNY_NUMBER = 42


def generate_hidato(width, height, alpha):
    gen = HidatoGenerator()
    return gen.generate_grid(width, height, alpha)


def _solve_csp(width, height, grid, select_variable, order_values, forward_checking, display):
    problem = HidatoCSP(width, height, grid)
    problem.display()

    gui = HidatoUI(problem, width)

    solver = CSPSolver(problem)
    solver.solve(select_variable, order_values, forward_checking)

    if display:
        gui.show_solve_steps(problem.moves)

    return problem, solver._num_of_iterations


def _solve_hill_climbing(width, height, grid, display):
    problem = HidatoSearchProblem(width, height, grid)
    problem.display()

    gui = HidatoUI(problem, width)

    solver = HillClimber()
    solver.solve(problem)

    if display:
        gui.show_solve_steps(problem.moves)

    return problem


def benchmark(width, height, alpha):
    select_variables_options = ["Ordered", "MRV"]
    order_values_options = ["Random", "LCV"]
    forward_checking = [True, False]

    results = []
    grid = generate_hidato(width, height, alpha)

    for select_var, order_values, fc in itertools.product(select_variables_options, order_values_options,
                                                          forward_checking):
        key = f"{select_var} & {order_values} & {fc}"

        running_time = []
        backtracking_steps = []
        for i in range(BENCHMARK_ITERATIONS):
            start = time.time()
            _, num_of_backtracking = _solve_csp(width, height, grid.copy(), select_var, order_values, fc, False)
            time_since = _time_since(start)
            running_time.append(time_since)
            backtracking_steps.append(num_of_backtracking)

        running_time = int(np.average(running_time) * MICROSECS_IN_SECS)
        num_of_backtracking = int(np.average(backtracking_steps))

        results.append((key, running_time, num_of_backtracking))

    export_results_to_csv(results)


def export_results_to_csv(results):
    df = pd.DataFrame(results, columns=["heuristic", "running time", "backtracking_steps"])
    df.to_csv('csp_runtimes.csv')


def main():
    args = parse_args()
    random.seed(THE_FUNNY_NUMBER)

    width = height = args.dimension

    if args.benchmark:
        benchmark(width, height, args.alpha)
        return

    print(f'Solving a {width} x {height} Hidato...\n')
    grid = generate_hidato(width, height, args.alpha)

    if args.hill_climbing:
        problem = _solve_hill_climbing(width, height, grid, args.gui)
    elif args.csp:
        problem, _ = _solve_csp(width, height, grid, select_variable="MRV", order_values="LCV", forward_checking=False,
                                display=args.gui)

    print("\nAfter solve:")
    sys.stdout.flush()
    problem.display()
    is_correct = problem.is_correct()
    print(f"Solution is {'correct' if is_correct else 'incorrect'}.")
    if not is_correct:
        loss = problem.get_loss(problem.board)
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
    parser.add_argument('--gui', dest='gui', action='store_true')
    return parser


if __name__ == '__main__':
    main()
