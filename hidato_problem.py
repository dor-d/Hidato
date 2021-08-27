import numpy as np

from Board import Board


class HidatoProblem:
    def __init__(self, width, height, grid):
        self.width = width
        self.height = height
        self.size = len(grid)
        grid = np.array(grid).reshape(self.height, self.width)
        self.board = Board(width, height, grid)

    def set_current_state(self, state: Board):
        self.board = state

    def is_correct(self):
        return self.board.is_correct()

    def is_complete(self):
        return self.board.is_complete()

    def display(self):
        self.board.display()