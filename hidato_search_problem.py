import numpy as np

from hidato_problem import HidatoProblem
from utils import EMPTY


class HidatoSearchProblem(HidatoProblem):
    def __init__(self, width, height, grid):
        super().__init__(width, height, grid)
        self.grid = np.array(grid).reshape(self.width, self.height)
        self.fixed_cells = self.grid != EMPTY

    def init_random_state(self):
        indices = self._get_unfixed_cells()
        indices = list(np.random.permutation(indices))
        fixed_numbers = self._get_fixed_numbers()
        for i in range(1, self.size + 1):
            if i not in fixed_numbers:
                x, y = indices.pop(0)
                self.grid[x, y] = i

        return self.grid

    def _get_unfixed_cells(self):
        return np.argwhere(self.fixed_cells == False)

    def _get_fixed_numbers(self):
        return self.grid[self.fixed_cells]

    def get_current_state(self):
        return self.grid

    def get_random_neighbor(self):
        neighbor = np.copy(self.grid)

        unfixed_cells = self._get_unfixed_cells()
        number_of_rows = unfixed_cells.shape[0]
        random_indices = np.random.choice(number_of_rows, size=2, replace=False)
        random_rows = unfixed_cells[random_indices, :]

        x_i, y_i = random_rows[0]
        x_j, y_j = random_rows[1]

        temp = neighbor[y_i, x_i]
        neighbor[y_i, x_i] = neighbor[y_j, x_j]
        neighbor[y_j, x_j] = temp

        return neighbor

    def set_current_state(self, state):
        self.grid = state

    def get_loss(self, state):
        loss = 0

        prev_index = self._get_index_in_state(state, 1)
        for i in range(2, self.size + 1):
            current_index = self._get_index_in_state(state, i)
            if not self._are_attached(*prev_index, *current_index):
                loss += 1

            prev_index = current_index

        return loss

    @staticmethod
    def _get_index_in_state(state, x):
        return tuple(np.argwhere(state == x)[0])

    def _2d_index(self, variable):
        return self._get_index_in_state(self.grid, variable)

    def get(self, x, y):
        return self.grid[x, y]
