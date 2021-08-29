from hidato_problem import HidatoProblem
from collections import namedtuple

Move = namedtuple('Move', ['index', 'number'])


class HidatoCSP(HidatoProblem):
    def __init__(self, width, height, grid):
        super().__init__(width, height, grid)
        self.domains = {}
        self._update()
        self.moves = []

    def get_variables(self):
        return range(1, self.size + 1)

    def initialize_domain(self):
        for x in self.get_variables():
            if self.board.is_assigned(x):
                self.domains[x] = [self.board._2d_index(x)]
            else:
                self.domains[x] = self.board.empty_cells.copy()

    def get_domain(self, x):
        return self.domains[x]

    def get_binary_constraints(self, x, y):
        if abs(y - x) != 1:
            return lambda a, b: True

        def constraint(a, b):
            return self.board._are_attached(*a, *b)

        return constraint

    def get_constraints(self, x):
        if self.board.is_assigned(x):
            return {self.board._2d_index(x)}

        elif x == 1 and self.board.is_assigned(2):
            return self.board._neighbors_of(2) & self.board.empty_cells

        elif x == self.size and self.board.is_assigned(x - 1):
            return self.board._neighbors_of(x - 1) & self.board.empty_cells

        else:
            return (self.board._neighbors_of(x - 1) if self.board.is_assigned(x - 1) else self.board.empty_cells) \
                   & (self.board._neighbors_of(x + 1) if self.board.is_assigned(x + 1) else self.board.empty_cells) \
                   & self.board.empty_cells

    def assign(self, variable, value):
        move = self.board.assign(variable, value)
        self.moves.append(move)

    def delete_assignment(self, variable):
        move = self.board.delete_assignment(variable)
        self.moves.append(move)

    def _update(self):
        self.initialize_domain()

    def empty_neighbors(self, x, y):
        return self.board.empty_neighbors(x, y)

    def get_arcs(self, variable):
        if variable == 1:
            arcs = [(2, 1)]
        elif variable == self.size:
            arcs = [(self.size - 1, variable)]
        else:
            arcs = [(variable - 1, variable), (variable + 1, variable)]
        return arcs


<<<<<<< Updated upstream
=======
    def __is_assigned(self, v):
        return self.board.is_assigned(v)

    def get_domains(self):
        return self.domains.copy()
>>>>>>> Stashed changes
