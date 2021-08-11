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

    def get_constraints(self, x):
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

    def _1d_to_2d_index(self, index):
        return index // self.width, index % self.width

    def _2d_index(self, variable):
        i = self.grid.index(variable)
        return self._1d_to_2d_index(i)

    def _1d_index(self, i, j):
        return i * self.width + j

    def _in_grid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

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
        self.domain = {self._1d_to_2d_index(i) for i in range(self.size) if self.grid[i] == EMPTY}

    def _update_assigned_variables(self):
        self.assigned_variables = {x for x in self.grid if x != EMPTY}

    def is_assigned(self, x):
        return x in self.assigned_variables

    def is_correct(self):
        return self.is_complete() and self.is_consistent()

    def is_complete(self):
        return len(self.assigned_variables) == len(self.get_variables())

    def is_consistent(self):
        index = self.grid.index(1)
        x_before = index // self.width
        y_before = index % self.width
        for i in range(2, self.width * self.height + 1):
            index = self.grid.index(i)
            x, y = index // self.width, index % self.width
            if abs(x_before - x) > 1 or abs(y_before - y) > 1:
                return False
            x_before = x
            y_before = y
        return True

    def empty_neighbors(self, x, y):
        return self._neighbors_of_index(x, y) & self.domain

    def display(self):
        for y in range(self.height):
            print((''.join(['+'] + ['--+' for _ in range(self.width)])))
            row = ['|']
            for x in range(self.width):
                i = y * self.width + x
                if self.grid[i] == -1:
                    row.append('* |')
                else:
                    row.append('%2d|' % self.grid[i])
            print((''.join(row)))
        print((''.join(['+'] + ['--+' for _ in range(self.width)])))
