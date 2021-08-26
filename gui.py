import math
from tkinter import Canvas, Frame, BOTH, TOP, Tk

import numpy as np

from hidato_problem import HidatoProblem
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

    def __init__(self, parent, problem: HidatoProblem, dim):
        self.problem = problem
        self.__view_grid = np.array(problem.grid).reshape(problem.height, problem.width)
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
        Draws grid divided with black lines into dimxdim squares.
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
                    self.__fill_cell(i, j, number)

    @staticmethod
    def _get_gui_position(j):
        return MARGIN + j * SIDE

    def __fill_cell(self, i, j, number, text_color='black', bg_color=None):
        x, y = self.__get_2d_gui_position(i, j)

        self.__create_grid_cell(x, y, number, text_color, bg_color)

        self.__view_grid[i, j] = number

    def __get_2d_gui_position(self, i, j):
        x = self._get_gui_position(i)
        y = self._get_gui_position(j)
        return x, y

    def __create_grid_cell(self, x, y, number, text_color, bg_color):
        z = self.__create_text(x, y, number, text_color)
        if bg_color is None:
            bg_color = self.colors[number - 1] if self.problem.is_variable_consistent(number) else "red"
        r = self.__create_rectangle(x, y, bg_color)
        self.canvas.tag_lower(r, z)

    def __create_text(self, x, y, number, color):
        z = self.canvas.create_text(
            x + SIDE / 2, y + SIDE / 2, text=number, tags=["numbers", self._tag(x, y)], fill=color
        )
        return z

    def __create_rectangle(self, x, y, bg_color):
        r = self.canvas.create_rectangle(x, y, x + SIDE, y + SIDE, fill=bg_color,
                                         tags=['numbers', self._tag(x, y)]
                                         )
        return r

    def show_solve_steps(self, steps):
        self.__update_gui_and_wait(START_WAIT_SECONDS)
        for step in steps:
            if isinstance(step, Move):
                self.__show_move(step)
            elif isinstance(step, Swap):
                self.__show_swap(step)
            elif isinstance(step, Board):
                self.__show_board(step)

            self.__update_gui_and_wait(STEP_WAIT_SECONDS)
        self.__wait(END_WAIT_SECONDS)

    def __show_move(self, move: Move):
        if move.number == EMPTY:
            self.__delete_from_cell(move.x_pos, move.y_pos)
        else:
            self.__fill_cell(*move, 'black')

    def __delete_from_cell(self, i, j):
        x, y = self.__get_2d_gui_position(i, j)
        self.canvas.delete(self._tag(x, y))
        self.__view_grid[i, j] = EMPTY

    def __show_swap(self, swap):
        """
         Used to make several consecutive moves without updating gui to give the appearance of a swap.
        :param change:
        :return:
        """
        # change color of swapped cells

        first_cell = (swap.x_1, swap.y_1)
        second_cell = (swap.x_2, swap.y_2)

        self.__flash_cell(*first_cell)
        self.__flash_cell(*second_cell)
        self.__update_gui_and_wait(STEP_WAIT_SECONDS)

        first_number = self.__view_grid[first_cell]
        second_number = self.__view_grid[second_cell]

        # delete swapped cells
        self.__delete_from_cell(*first_cell)
        self.__delete_from_cell(*second_cell)
        self.__update_gui_and_wait(STEP_WAIT_SECONDS / math.pi)

        # fill swapped cells
        self.__fill_cell(*first_cell, second_number)
        self.__fill_cell(*second_cell, first_number)

        # for move in change.swap_moves_list[NUM_DELETE_MOVES_IN_SWAP:]:
        #     self.__change_bg_color(move.x_pos, move.y_pos, bg_color='gold')
        # self.__update_gui_and_wait(STEP_WAIT_SECONDS)
        # for move in change.swap_moves_list[NUM_DELETE_MOVES_IN_SWAP:]:
        #     self.__change_bg_color(move.x_pos, move.y_pos, bg_color=None)

    def __flash_cell(self, i, j):
        self.__change_bg_color(i, j, bg_color='gold')

    def __change_bg_color(self, x, y, bg_color):
        number = self.problem.get(x, y)
        self.__fill_cell(x, y, number, bg_color=bg_color)

    def __show_board(self, board: Board):
        self.canvas.delete("numbers")
        for i in range(self.dim):
            for j in range(self.dim):
                number = board.grid[i, j]
                if number != EMPTY:
                    self.__fill_cell(i, j, number, 'black')

    def __update_gui_and_wait(self, wait_duration):
        self.__update_gui()
        self.__wait(wait_duration)

    def __update_gui(self):
        self.parent.update_idletasks()
        self.parent.update()

    @staticmethod
    def __wait(duration):
        return time.sleep(duration)

    @staticmethod
    def _tag(x, y):
        return f'({x, y})'
