from CSP import CSP

EMPTY = -1


class HidatoCSP(CSP):

    def __init__(self, width, height, grid):
        self.width = width
        self.height = height
        self.size = len(grid)
        self.grid = grid
        self._update()

    def get_variables(self):
        return list(range(1, self.size + 1))

    def get_domain(self, x):
        return self.domain

    def get_constraint(self, x):
        if x in self.assigned_variables:
            return {self._2d_index(x)}

        if x == 1 and 2 in self.assigned_variables:
            return self._neighbors_of(2) & self.domain

        if 1 < x < self.size:
            return (self._neighbors_of(x - 1) if x - 1 in self.assigned_variables else self.domain) \
                   & (self._neighbors_of(x + 1) if x + 1 in self.assigned_variables else self.domain) \
                   & self.domain

        if x == self.size and x - 1 in self.assigned_variables:
            return self._neighbors_of(x - 1) & self.domain

        return set()

    def _neighbors_of(self, variable):
        if variable not in self.assigned_variables:
            raise ValueError()

        x, y = self._2d_index(variable)
        return self._neighbors_of_index(x, y)

    def _neighbors_of_index(self, x, y):
        return {(x + i, y + j)
                for i in range(-1, 2)
                for j in range(-1, 2)
                if self._in_grid(x + i, y + j)
                }

    def _2d_index(self, variable):
        i = self.grid.index(variable)
        return i // self.width, i % self.width

    def _1d_index(self, i, j):
        return i * self.width + j

    def _in_grid(self, x, y):
        return x < 0 or x > self.width or y < 0 or y > self.height

    def assign(self, x, value):
        index = self._1d_index(*value)
        if self.grid[index] != EMPTY:
            raise ValueError(f"Index {value} already assigned to a variable.")
        self.grid[index] = x
        self._update()

    def delete_assignment(self, variable):
        if variable not in self.assigned_variables:
            raise ValueError(f"Variable {variable} not assigned.")
        index = self.grid.index(variable)
        self.grid[index] = EMPTY
        self._update()

    def _update(self):
        self._update_domain()
        self._update_assigned_variables()

    def _update_domain(self):
        self.domain = {self._2d_index(i) for i in range(self.size) if self.grid[i] == EMPTY}

    def _update_assigned_variables(self):
        self.assigned_variables = {x for x in self.grid if x != EMPTY}

    def is_assigned(self, x):
        return x in self.assigned_variables

    def is_complete(self):
        return len(self.assigned_variables) == len(self.get_variables())

    def empty_neighbors(self, x, y):
        return self._neighbors_of_index(x, y) & self.domain

