import numpy as np

from utils import EMPTY, Board, Move, Swap

NUM_OF_MOVES_IN_SWAP = 4


# Swap = namedtuple('Swap', ['first', 'second'])


class HidatoSearchProblem:
    def __init__(self, width, height, grid):
        self.shape = (width, height)
        self.size = len(grid)
        self.grid = np.array(grid).reshape(self.shape)
        self.fixed_cells = self.grid != EMPTY
        self.moves = []

    def init_random_state(self):
        indices = self._get_unfixed_cells()
        indices = list(np.random.permutation(indices))
        fixed_numbers = self._get_fixed_numbers()
        for i in range(1, self.size + 1):
            if i not in fixed_numbers:
                x, y = indices.pop(0)
                self.grid[x, y] = i

        self.moves.append(Board(self.grid))
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

        # self.moves.append(Swap((x_i, y_i), (x_j, y_j)))
        self._add_swap_moves(x_i, y_i, x_j, y_j)

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

    def is_complete(self):
        return EMPTY not in self.grid

    def is_consistent(self):
        prev_x, prev_y = self._get_index_in_state(self.grid, 1)

        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                if not self._are_attached(x, y, prev_x, prev_y):
                    return False

                prev_x, prev_y = x, y

        return True

    @staticmethod
    def _are_attached(x1, y1, x2, y2):
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1 and (x1 != x2 or y1 != y2)

    def is_correct(self):
        return self.is_complete() and self.is_consistent()

    def remove_last_move(self):
        self.moves.pop(-1)

    def get(self, x, y):
        return self.grid[x, y]

    def _add_swap_moves(self, x1, y1, x2, y2):
        first_number = self.get(x1, y1)
        second_number = self.get(x2, y2)
        self.moves.append(
            Swap(swap_moves_list=[
                Move(x1, y1, EMPTY),
                Move(x2, y2, EMPTY),
                Move(x1, y1, second_number),
                Move(x2, y2, first_number)
            ])
        )

    def pop_swap_from_moves(self):
        """
        Use to pop last moves added by a previous call to _add_swap_moves.
        :return:
        """
        if len(self.moves) > 0 and isinstance(self.moves[-1], Swap):
            self.moves.pop(-1)
        else:
            raise RuntimeWarning('Tried to pop swap with no swap in moves.')
