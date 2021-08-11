from HidatoGenerator import *
from HidatoCSP import *
from SolverCSP import *

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