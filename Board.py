import numpy as np

from utils import Move

EMPTY = -1


class Board:
    def __init__(self, width, height, grid):
        self.width = width
        self.height = height
        self.size = width * height
        self.grid = np.copy(grid)
        self.empty_cells = set()
        self.update()

    def is_assigned(self, x):
        return x in self.grid

    def is_complete(self):
        return EMPTY not in self.grid

    def is_consistent(self):
        prev_y, prev_x = self._2d_index(1)

        for i in range(2, self.width * self.height + 1):
            y, x = self._2d_index(i)
            if not self._are_attached(y, x, prev_y, prev_x):
                return False

            prev_y, prev_x = y, x
        return True

    def is_correct(self):
        return self.is_complete() and self.is_consistent()

    def get(self, x, y):
        return self.grid[x, y]

    def _2d_index(self, variable):
        return np.argwhere(self.grid == variable)[0]

    def _is_in_grid(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    @staticmethod
    def _surrounding_indices(x, y):
        return {
            (x + j, y + i)
            for i in range(-1, 2)
            for j in range(-1, 2)
        }

    def _neighbors_of_index(self, x, y):
        return {(i, j) for i, j in self._surrounding_indices(x, y) if self._is_in_grid(i, j)}

    def _neighbors_of(self, variable):
        if not self.is_assigned(variable):
            raise ValueError(f"The variable {variable} is not assigned.")

        x, y = self._2d_index(variable)
        return self._neighbors_of_index(x, y)

    def _is_variable_consistent(self, variable):
        is_not_consistent = True
        x_0, y_0 = self._2d_index(variable)

        if variable == 1 and self.is_assigned(2):
            x_i, y_i = self._2d_index(2)
            is_not_consistent = self._are_attached(x_0, y_0, x_i, y_i)

        elif variable == self.size and self.is_assigned(variable - 1):
            x_i, y_i = self._2d_index(self.size - 1)
            is_not_consistent = self._are_attached(x_0, y_0, x_i, y_i)

        elif self.is_assigned(variable - 1) and self.is_assigned(variable + 1):
            x_i, y_i = self._2d_index(variable + 1)
            x_j, y_j = self._2d_index(variable - 1)
            is_not_consistent = self._are_attached(x_0, y_0, x_i, y_i) and self._are_attached(x_0, y_0, x_j, y_j)

        return is_not_consistent

    @staticmethod
    def _are_attached(x1, y1, x2, y2):
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1 and (x1 != x2 or y1 != y2)

    def display(self):
        for x in range(self.height):
            print((''.join(['+'] + ['--+' for _ in range(self.width)])))
            row = ['|']
            for y in range(self.width):
                val = self.get(x, y)
                if val == EMPTY:
                    row.append('* |')
                else:
                    row.append('%2d|' % val)
            print((''.join(row)))
        print((''.join(['+'] + ['--+' for _ in range(self.width)])))

    def assign(self, variable, value):
        if self.grid[value] != EMPTY:
            raise ValueError(f"Index {value} already assigned to a variable.")

        self.grid[value] = variable
        self.update()
        return Move(*value, variable)

    def delete_assignment(self, variable):
        index = self._2d_index(variable)
        self.grid[index] = EMPTY
        self.update()
        return Move(*index, EMPTY)

    def update(self):
        self.empty_cells = {tuple(row) for row in np.argwhere(self.grid == EMPTY)}

    def empty_neighbors(self, x, y):
        return self._neighbors_of_index(x, y) & self.empty_cells
