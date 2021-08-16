import argparse
import random
import sys

from HidatoGenerator import HidatoGenerator
from SolverCSP import SolverCSP
from utils import timeit

DIM = 13


@timeit
def generate_hidato(width, height):
    # For debug purpose
    random.seed(0)

    print(f'Solving a {width} x {height} Hidato...\n')

    gen = HidatoGenerator()
    hidato = gen.generateHidato(width, height, alpha=0.5)
    print("Before solve:")
    hidato.display()

    sys.stdout.flush()

    return hidato


@timeit
def _solve(hidato, **kwargs):
    print("\nAfter solve:")

    solver = SolverCSP()
    solver.solve(hidato, **kwargs)
    hidato.display()

    print(f"Solution is {'correct' if hidato.is_correct() else 'incorrect'}.")


def main():
    width = height = DIM
    hidato = generate_hidato(width, height)
    _solve(hidato, select_variable="MRV", order_values="LCV", forward_checking=True)


def benchmark():
    width = height = DIM
    hidato = generate_hidato(width, height)
    time_with_fc = _solve(hidato, select_variable="MRV", order_values="LCV", forward_checking=True)
    time_without_fc = _solve(hidato, select_variable="MRV", order_values="LCV", forward_checking=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hidato Solver')
    parser.add_argument('--benchmark', dest='benchmark', action='store_true')
    args = parser.parse_args()

    if args.benchmark:
        benchmark()
    else:
        main()
