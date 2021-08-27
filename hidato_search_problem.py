import numpy as np

from Board import Board
from hidato_problem import HidatoProblem
from utils import EMPTY, Swap

NUM_OF_MOVES_IN_SWAP = 4


class HidatoSearchProblem(HidatoProblem):
    def __init__(self, width, height, grid):
        super().__init__(width, height, grid)
        self.fixed_cells = self.board.grid != EMPTY
        self.moves = []

    def get_random_state(self):
        indices = self._get_unfixed_cells()
        indices = list(np.random.permutation(indices))
        fixed_numbers = self._get_fixed_numbers()
        random_state = self.board.copy()
        for i in range(1, self.width * self.height + 1):
            if i not in fixed_numbers:
                random_state[tuple(indices.pop(0))] = i

        self.moves.append(Board(self.width, self.height, random_state.grid))

        return random_state

    def _get_unfixed_cells(self):
        return np.argwhere(self.fixed_cells == False)

    def _get_fixed_numbers(self):
        return self.board.grid[self.fixed_cells]

    def get_random_neighbor(self):
        neighbor = np.copy(self.board.grid)

        unfixed_cells = self._get_unfixed_cells()
        number_of_rows = unfixed_cells.shape[0]
        random_indices = np.random.choice(number_of_rows, size=2, replace=False)
        random_rows = unfixed_cells[random_indices, :]

        y_i, x_i = random_rows[0]
        y_j, x_j = random_rows[1]

        temp = neighbor[y_i, x_i]
        neighbor[y_i, x_i] = neighbor[y_j, x_j]
        neighbor[y_j, x_j] = temp

        self.moves.append(Swap(x_i, y_i, x_j, y_j))

        return Board(self.width, self.height, neighbor)

    def get_loss(self, state: Board):
        loss = 0

        prev_index = state._2d_index(1)
        for i in range(2, self.size + 1):
            current_index = state._2d_index(i)
            if not Board._are_attached(*prev_index, *current_index):
                loss += 1

            prev_index = current_index

        return loss

    def remove_last_move(self):
        self.moves.pop(-1)

    def undo_last_move(self):
        """
        Use to pop last moves added by a previous call to _add_swap_moves.
        :return:
        """
        if len(self.moves) > 0:
            self.moves.pop(-1)
        else:
            raise RuntimeWarning('Tried to undo move with no moves made.')
