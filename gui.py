from tkinter import Canvas, Frame, BOTH, TOP, Tk

import hidato_csp
import hidato_search_problem
from utils import EMPTY, Move, Board, Swap
import time

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
START_WAIT_SECONDS = 3
STEP_WAIT_SECONDS = 0.8
END_WAIT_SECONDS = 15
NUM_DELETE_MOVES_IN_SWAP = 2


class HidatoUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """

    def __init__(self, parent, problem, dim):
        self.problem = problem
        Frame.__init__(self, parent)
        self.parent = parent
        self.dim = dim
        self.size = MARGIN * 2 + SIDE * dim

        self.row, self.col = -1, -1

        self.colors = []
        color_start = 94
        color_end = 255
        step = int((color_end - color_start) / self.dim ** 2)
        other_color = 0

        current_color = color_start
        for i in range(1, self.dim ** 2 + 1):
            self.colors.append(self._from_rgb(other_color, current_color, other_color))
            current_color += step
            other_color += step

        self.__initUI()


    @staticmethod
    def _from_rgb(r, g, b):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        # r, g, b = num >> 16, (num >> 8) & 0xFF, num & 0xFF
        return f'#{r:02x}{g:02x}{b:02x}'

    def __initUI(self):
        self.parent.title("Hidato")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=self.size,
                             height=self.size)
        self.canvas.pack(fill=BOTH, side=TOP)

        self.__draw_grid()
        self.__draw_puzzle()

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(self.dim + 1):
            color = "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = self.size - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = self.size - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(self.dim):
            for j in range(self.dim):
                number = self.problem.get(i, j)
                if number != EMPTY:
                    x = self._get_gui_position(j)
                    y = self._get_gui_position(i)
                    self.__fill_cell(number, 'black', x, y)

    @staticmethod
    def _get_gui_position(j):
        return MARGIN + j * SIDE

    def __fill_cell(self, number, color, x, y):
        z = self.canvas.create_text(
            x + SIDE / 2, y + SIDE / 2, text=number, tags=["numbers", self._tag(x, y)], fill=color
        )
        r = self.canvas.create_rectangle(x, y, x + SIDE, y + SIDE, fill=self.colors[number - 1],
                                         tags=[self._tag(x, y)]
                                         )

        self.canvas.tag_lower(r, z)

    def show_solve_steps(self, steps):
        self.__update_gui()
        self.__wait(START_WAIT_SECONDS)
        for step in steps:
            if isinstance(step, Move):
                self._make_move(step)
            elif isinstance(step, Swap):
                self._make_swap(step)
            elif isinstance(step, hidato_search_problem.Board):
                self._make_board(step)

            self.__update_gui()
            self.__wait(STEP_WAIT_SECONDS)
        self.__wait(END_WAIT_SECONDS)

    @staticmethod
    def __wait(duration):
        return time.sleep(duration)

    def _make_move(self, move: Move):
        x = self._get_gui_position(move.x_pos)
        y = self._get_gui_position(move.y_pos)
        if move.number == EMPTY:
            self._delete_from_cell(x, y)
        else:
            self.__fill_cell(move.number, 'black', x, y)

    def _delete_from_cell(self, x, y):
        self.canvas.delete(self._tag(x, y))

    def _make_swap(self, change):
        """
         Used to make several consecutive moves without updating gui to give the appearance of a swap.
        :param change:
        :return:
        """
        for move in change.swap_moves_list[:NUM_DELETE_MOVES_IN_SWAP]:
            self._make_move(move)
        self.__update_gui()
        self.__wait(STEP_WAIT_SECONDS / 2)
        for move in change.swap_moves_list[NUM_DELETE_MOVES_IN_SWAP:]:
            self._make_move(move)

    def _make_board(self, board: hidato_search_problem.Board):
        self.canvas.delete("numbers")
        for i in range(self.dim):
            for j in range(self.dim):
                number = board.grid[i, j]
                if number != EMPTY:
                    x = self._get_gui_position(j)
                    y = self._get_gui_position(i)
                    self.__fill_cell(number, 'black', x, y)

    def __update_gui(self):
        self.parent.update_idletasks()
        self.parent.update()

    @staticmethod
    def _tag(x, y):
        return f'({x, y})'
