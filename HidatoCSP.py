from CSP import CSP

EMPTY = -1


class HidatoCSP(CSP):

    def __init__(self, width, height, grid):
        self.width = width
        self.height = height
        self.size = len(grid)
        self.grid = grid
        self.domains = {}
        self._update()

    def get_variables(self):
        return list(range(1, self.size + 1))

    def initialize_domain(self):
        default_domain = [self._1d_to_2d_index(i) for i in range(self.size) if self.grid[i] == EMPTY]
        for x in self.get_variables():
            if x in self.assigned_variables:
                self.domains[x] = [self._2d_index(x)]
            else:
                self.domains[x] = default_domain.copy()


    def get_domain(self, x):
        return self.domains[x]

    def get_constraints_between(self, x, y):
        if (abs(y - x) != 1):
            return lambda a, b: True

        def constraint(a,b):
            return a != b and abs(a[1] - b[1]) <= 1 and abs(a[0] - b[0]) <= 1

        return constraint

    def get_constraints(self, x):
        if self._is_assigned(x):
            return {self._2d_index(x)}

        if x == 1 and 2 in self.assigned_variables:
            return self._neighbors_of(2) & self.domain

        if 1 < x < self.size:
            return (self._neighbors_of(x - 1) if self._is_assigned(x - 1) else self.domain) \
                   & (self._neighbors_of(x + 1) if self._is_assigned(x + 1) else self.domain) \
                   & self.domain

        if x == self.size and self._is_assigned(x - 1):
            return self._neighbors_of(x - 1) & self.domain

        return set()

    def _neighbors_of(self, variable):
        if not self._is_assigned(variable):
            raise ValueError()

        x, y = self._2d_index(variable)
        return self._neighbors_of_index(x, y)

    def _is_assigned(self, x):
        return x in self.assigned_variables

    def _neighbors_of_index(self, x, y):
        return {(i, j) for i, j in self._surrounding_indices(x, y) if self._in_grid(i, j)}

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

    def _in_grid(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    def assign(self, x, value):
        index = self._1d_index(*value)
        if self.grid[index] != EMPTY:
            raise ValueError(f"Index {value} already assigned to a variable.")
        self.grid[index] = x
        self._update()

    def delete_assignment(self, variable):
        index = self._1d_index_of(variable)
        self.grid[index] = EMPTY
        self._update()

    def _1d_index_of(self, x):
        if x not in self.assigned_variables:
            raise ValueError(f"Variable {x} not assigned.")
        return self.grid.index(x)

    def _update(self):
        self._update_domain()
        self._update_assigned_variables()
        self.initialize_domain()

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
        x_before, y_before = self._2d_index(1)
        for i in range(2, self.size + 1):
            x, y = self._2d_index(i)
            if not self._are_attached(x, y, x_before, y_before):
                return False
            x_before, y_before = x, y
        return True

    def _are_attached(self, x1, y1, x2, y2):
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1 and (x1 != x2 or y1 != y2)

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
