import sys
import random

from HidatoGenerator import HidatoGenerator
from SolverCSP import SolverCSP
from utils import timeit

DIM = 13


@timeit
def solve_hidato(width, height):
    print(f'Solving a {width} x {height} Hidato...\n')

    gen = HidatoGenerator()
    hidato = gen.generateHidato(width, height, alpha=0.5)
    print("Before solve:")
    hidato.display()

    sys.stdout.flush()

    print("\nAfter solve:")
    _solve(hidato)
    hidato.display()

    print(f"Solution is {'correct' if hidato.is_correct() else 'incorrect'}.")


@timeit
def _solve(hidato):
    solver = SolverCSP()
    solver.solve(hidato, "MRV", "LCV", forward_checking=True)


def main():
    random.seed(0)
    width = height = DIM
    solve_hidato(width, height)


if __name__ == '__main__':
    main()
