from copy import deepcopy

from hidato_problem import HidatoProblem
from collections import namedtuple

Move = namedtuple('Move', ['index', 'number'])


class HidatoCSP(HidatoProblem):
    def __init__(self, width, height, grid):
        super().__init__(width, height, grid)
        self.domains = {}
        self.__initialize_domains()
        self.moves = []

    def get_variables(self):
        return range(1, self.size + 1)

    def __initialize_domains(self):
        self.domains = {x: self.get_constraints(x) for x in self.get_variables()}

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
            return self.board.neighbors_of(2) & self.board.empty_cells

        elif x == self.size and self.board.is_assigned(x - 1):
            return self.board.neighbors_of(x - 1) & self.board.empty_cells

        else:
            return (self.board.neighbors_of(x - 1) if self.board.is_assigned(x - 1) else self.board.empty_cells) \
                   & (self.board.neighbors_of(x + 1) if self.board.is_assigned(x + 1) else self.board.empty_cells) \
                   & self.board.empty_cells

    def assign(self, variable, value):
        move = self.board.assign(variable, value)
        self.moves.append(move)
        self.domains[variable] = {value}
        self.__update_domains_after_assignment(variable, value)

    def delete_assignment(self, variable, old_domains):
        move = self.board.delete_assignment(variable)
        self.moves.append(move)
        self.domains = old_domains

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

    def get_unassigned_variables(self):
        return [v for v in self.get_variables() if not self.__is_assigned(v)]

    def __is_assigned(self, v):
        return self.board.is_assigned(v)

    def get_domains_copy(self):
        return deepcopy(self.domains)

    def __update_domains_after_assignment(self, variable, value):
        self.domains[variable] = {value}
        self.__update_consecutive_domains_after_assignment(variable)
        self.__remove_value_from_other_domains(variable, value)

    def __update_consecutive_domains_after_assignment(self, variable):
        neighbors = self.board.neighbors_of(variable)
        if variable > 1:
            self.domains[variable - 1] &= neighbors
        if variable < self.size:
            self.domains[variable + 1] &= neighbors

    def __remove_value_from_other_domains(self, variable, value):
        for other in self.domains.keys():
            if other != variable and value in self.domains[other]:
                self.domains[other].remove(value)


