import itertools
import random

import numpy as np

from Board import Board
from hidato_problem import HidatoProblem
from utils import EMPTY, Swap

NUM_OF_MOVES_IN_SWAP = 4


class HidatoSearchProblem(HidatoProblem):
    def __init__(self, width, height, grid):
        super().__init__(width, height, grid)
        self.fixed_cells = self.board.grid != EMPTY

        fixed_numbers = self._get_fixed_numbers()
        self.unfixed_numbers = [num for num in range(1, self.size + 1) if num not in fixed_numbers]
        self.moves = []

    def get_current_state(self):
        return self.board

    def init_random_state(self):
        random_state = self.get_random_state()
        self.set_current_state(random_state)
        self.moves.append(Board(self.width, self.height, random_state.grid))

    def get_random_state(self):
        indices = self._get_unfixed_cells()
        indices = list(np.random.permutation(indices))
        fixed_numbers = self._get_fixed_numbers()
        random_state = self.board.copy()
        for i in range(1, self.width * self.height + 1):
            if i not in fixed_numbers:
                random_state[tuple(indices.pop(0))] = i

        return random_state

    def _get_unfixed_cells(self):
        return [tuple(v) for v in np.argwhere(self.fixed_cells == False)]

    def _get_fixed_numbers(self):
        return self.board.grid[self.fixed_cells]

    def move_to_first_better_neighbor(self):
        for first_cell, second_cell in itertools.combinations(self._get_unfixed_cells(), 2):
            if self.__swap_if_loss_improves(*first_cell, *second_cell):
                return True
        return False

    def __swap_if_loss_improves(self, x_1, y_1, x_2, y_2):
        loss_before_swap = self.get_current_loss()
        self.__swap(x_1, y_1, x_2, y_2)
        if self.get_current_loss() < loss_before_swap:
            self.moves.append(Swap(x_1, y_1, x_2, y_2))
            return True
        self.__swap(x_1, y_1, x_2, y_2)
        return False

    def get_current_loss(self):
        return self.get_loss(self.board)

    def get_random_neighbor(self):
        unfixed_cells = self._get_unfixed_cells()
        first_cell, second_cell = random.sample(unfixed_cells, 2)

        self.__swap(*first_cell, *second_cell)
        self.moves.append(Swap(*first_cell, *second_cell))

        return True

    def get_neighbor_by_swapping(self, x_i, y_i, x_j, y_j):
        neighbor = np.copy(self.board.grid)

        temp = neighbor[y_i, x_i]
        neighbor[y_i, x_i] = neighbor[y_j, x_j]
        neighbor[y_j, x_j] = temp

        board = Board(self.width, self.height, neighbor)

        return board

    def get_loss(self, state: Board):
        loss = 0

        prev_index = state._2d_index(1)
        for i in self.unfixed_numbers:
            current_index = state._2d_index(i)
            if not Board._are_attached(*prev_index, *current_index):
                loss += 1

            prev_index = current_index

        return loss / self.size

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

    def __swap(self, x_1, y_1, x_2, y_2):
        first, second = self.board[x_1, y_1], self.board[x_2, y_2]
        self.board[x_1, y_1], self.board[x_2, y_2] = second, first
