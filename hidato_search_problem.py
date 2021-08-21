import itertools

import numpy as np

EMPTY = -1
from simpleai.search import SearchProblem


class HidatoSearchProblem(SearchProblem):

    def __init__(self, width, height, grid):
        self.shape = (width, height)
        self.size = len(grid)
        self.grid = np.array(grid).reshape(self.shape)
        self.fixed_cells = self.grid != EMPTY

        self.clean_state = {}
        for i in range(width):
            for j in range(height):
                val = self.grid[j, i]
                self.clean_state[val] = (i, j)

        self.unfixed_values = set(range(1, self.size+1)) - set(self.grid[self.fixed_cells == True])

        initial_state = self.generate_random_state()
        super().__init__(initial_state)

    def init_random_state(self):
        self.grid = self.generate_random_state()
        return self.grid

    def actions(self, state):
        return itertools.combinations(self.unfixed_values, 2)

    def result(self, state, action):
        '''Returns the resulting state of applying `action` to `state`.'''

        i, j = action

        new_state = dict(state)

        temp = new_state[j]
        new_state[j] = new_state[i]
        new_state[i] = temp

        return new_state

    def generate_random_state(self):
        """
        SimpleAi
        :return:
        """
        grid = dict(self.clean_state)

        indices = self._get_unfixed_cells()
        indices = list(np.random.permutation(indices))
        fixed_numbers = self._get_fixed_numbers()
        for i in range(1, self.size + 1):
            if i not in fixed_numbers:
                x, y = indices.pop(0)
                grid[i] = (x, y)

        return grid


    def _get_unfixed_cells(self):
        x = np.argwhere(self.fixed_cells == False)
        return [list(v) for v in x]

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

    def value(self, state):
        """
        SimpleAi
        :param state:
        :return:
        """
        score = 0

        prev_index = state[1]
        for i in range(2, self.size + 1):
            current_index = state[i]
            if not self._is_attached(prev_index, current_index):
                score += 1

            prev_index = current_index

        return score

    @staticmethod
    def _get_index_in_state(state, x):
        state_np = np.array(state)
        return tuple(np.argwhere(state_np == x)[0])

    @staticmethod
    def _is_attached(a_index, b_index):
        return abs(a_index[0] - b_index[0]) <= 1 and abs(a_index[1] - b_index[1]) <= 1 and a_index != b_index

    def display(self):
        for x in range(self.shape[0]):
            print((''.join(['+'] + ['--+' for _ in range(self.shape[1])])))
            row = ['|']
            for y in range(self.shape[1]):
                # i = y * self.shape[1] + x
                if self.grid[x, y] == EMPTY:
                    row.append('* |')
                else:
                    row.append('%2d|' % self.grid[x, y])
            print((''.join(row)))
        print((''.join(['+'] + ['--+' for _ in range(self.shape[1])])))

