import numpy as np

EMPTY = -1


class HidatoSearchProblem:

    def __init__(self, width, height, grid):
        self.shape = (width, height)
        self.size = len(grid)
        self.grid = np.array(grid).reshape(self.shape)
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
        i, j = np.random.choice(self._get_unfixed_cells(), 2)
        neighbor[i], neighbor[j] = self.grid[j], self.grid[i]
        return neighbor

    def set_current_state(self, state):
        self.grid = state

    def get_loss(self, state):
        loss = 0

        prev_index = self._get_index_in_state(state, 1)
        for i in range(2, self.size + 1):
            current_index = self._get_index_in_state(state, i)
            if not self._is_attached(prev_index, current_index):
                loss += 1

            prev_index = current_index

        return loss

    @staticmethod
    def _get_index_in_state(state, x):
        return tuple(np.argwhere(state == x)[0])

    @staticmethod
    def _is_attached(a_index, b_index):
        return abs(a_index[0] - b_index[0]) <= 1 and abs(a_index[1] - b_index[1]) <= 1 and a_index != b_index
