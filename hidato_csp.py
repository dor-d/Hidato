from hidato_problem import HidatoProblem
from utils import EMPTY
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
            if self.is_assigned(x):
                self.domains[x] = [self._2d_index(x)]
            else:
                self.domains[x] = self.empty_cells.copy()

    def get_domain(self, x):
        return self.domains[x]

    def get_binary_constraints(self, x, y):
        if abs(y - x) != 1:
            return lambda a, b: True

        def constraint(a, b):
            return self._are_attached(*a, *b)

        return constraint

    def get_constraints(self, x):
        if self.is_assigned(x):
            return {self._2d_index(x)}

        elif x == 1 and self.is_assigned(2):
            return self._neighbors_of(2) & self.empty_cells

        elif x == self.size and self.is_assigned(x - 1):
            return self._neighbors_of(x - 1) & self.empty_cells

        else:
            return (self._neighbors_of(x - 1) if self.is_assigned(x - 1) else self.empty_cells) \
                   & (self._neighbors_of(x + 1) if self.is_assigned(x + 1) else self.empty_cells) \
                   & self.empty_cells

    def _neighbors_of(self, variable):
        if not self.is_assigned(variable):
            raise ValueError(f"The variable {variable} is not assigned.")

        x, y = self._2d_index(variable)
        return self._neighbors_of_index(x, y)

    def _neighbors_of_index(self, x, y):
        return {(i, j) for i, j in self._surrounding_indices(x, y) if self._is_in_grid(i, j)}

    @staticmethod
    def _surrounding_indices(x, y):
        return {
            (x + i, y + j)
            for i in range(-1, 2)
            for j in range(-1, 2)
        }

    def _1d_to_2d_index(self, index):
        return index // self.width, index % self.width

    def _2d_index(self, variable):
        i = self._1d_index_of(variable)
        return self._1d_to_2d_index(i)

    def _1d_index(self, i, j):
        return i * self.width + j

    def _1d_index_of(self, x):
        if not self.is_assigned(x):
            raise ValueError(f"Variable {x} not assigned.")
        return self.grid.index(x)

    def _is_in_grid(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    def assign(self, x, value):
        index = self._1d_index(*value)
        if self.grid[index] != EMPTY:
            raise ValueError(f"Index {value} already assigned to a variable.")
        self.grid[index] = x
        self._update()
        self.moves.append(Move(index, x))

    def delete_assignment(self, variable):
        index = self._1d_index_of(variable)
        self.grid[index] = EMPTY
        self._update()
        self.moves.append(Move(index, EMPTY))

    def _update(self):
        self._update_empty_cells()
        self.initialize_domain()

    def _update_empty_cells(self):
        self.empty_cells = {self._1d_to_2d_index(i) for i in range(self.size) if self.grid[i] == EMPTY}

    def empty_neighbors(self, x, y):
        return self._neighbors_of_index(x, y) & self.empty_cells

    def get_arcs(self, variable):
        if variable == 1:
            arcs = [(2, 1)]
        elif variable == self.size:
            arcs = [(self.size - 1, variable)]
        else:
            arcs = [(variable - 1, variable), (variable + 1, variable)]
        return arcs

    def get(self, x, y):
        i = self._1d_index(x, y)
        return self.grid[i]
