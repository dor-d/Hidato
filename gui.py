import math
from tkinter import Canvas, Frame, BOTH, TOP, Tk, messagebox

from matplotlib import cm

from hidato_problem import HidatoProblem
from utils import EMPTY, Move, Swap
from Board import Board
import time

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
START_WAIT_SECONDS = 0
STEP_WAIT_SECONDS = 0.15
SHORT_STEP_WAIT_SECONDS = STEP_WAIT_SECONDS / math.pi
END_WAIT_SECONDS = 15
NUM_DELETE_MOVES_IN_SWAP = 2

COLORMAP = cm.get_cmap('Greens')
ERROR_COLOR = 'red'
EMPTY_COLOR = 'white'
FLASH_COLOR = 'DarkGoldenrod1'
GRID_COLOR = 'gray'


class HidatoUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """

    def __init__(self, problem: HidatoProblem, dim):
        self.problem = problem
        self.__view_board = problem.board.copy()
        self.parent = Tk()
        Frame.__init__(self, self.parent)
        self.dim = dim
        self.size = MARGIN * 2 + SIDE * dim

        self.__initUI()

    def __initUI(self):
        self.parent.title("Hidato")
        self.pack(fill=BOTH)
        self.__create_canvas()
        self.__draw_grid()
        self.__draw_puzzle()

    def __create_canvas(self):
        self.canvas = Canvas(self,
                             width=self.size,
                             height=self.size)
        self.canvas.pack(fill=BOTH, side=TOP)

    def __draw_grid(self):
        """
        Draws grid divided with black lines into dimxdim squares.
        """
        for i in range(self.dim + 1):
            self.__draw_ith_cell(i)

    def __draw_ith_cell(self, i):
        x0 = MARGIN + i * SIDE
        y0 = MARGIN
        x1 = MARGIN + i * SIDE
        y1 = self.size - MARGIN
        self.canvas.create_line(x0, y0, x1, y1, fill=GRID_COLOR)

        x0 = MARGIN
        y0 = MARGIN + i * SIDE
        x1 = self.size - MARGIN
        y1 = MARGIN + i * SIDE
        self.canvas.create_line(x0, y0, x1, y1, fill=GRID_COLOR)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(self.dim):
            for j in range(self.dim):
                number = self.__view_board[i, j]
                if number != EMPTY:
                    self.__fill_cell(i, j, number)

    @staticmethod
    def _get_gui_position(j):
        return MARGIN + j * SIDE

    def __fill_cell(self, i, j, number, text_color='black', bg_color=None):
        x, y = self.__get_2d_gui_position(i, j)

        self.__view_board[i, j] = number

        self.__create_grid_cell(x, y, number, text_color, bg_color)

    def __get_2d_gui_position(self, i, j):
        y = self._get_gui_position(i)
        x = self._get_gui_position(j)
        return x, y

    def __create_grid_cell(self, x, y, number, text_color, bg_color):
        z = self.__create_text(x, y, number, text_color)

        if bg_color is None:
            bg_color = self.__choose_bg_color(number)

        r = self.__create_rectangle(x, y, bg_color)
        self.canvas.tag_lower(r, z)

    def __create_text(self, x, y, text, color):
        if text == EMPTY:
            text = ''
        z = self.canvas.create_text(
            x + SIDE / 2, y + SIDE / 2, text=text, tags=["numbers", self._tag(x, y)], fill=color
        )
        return z

    def __choose_bg_color(self, number):
        if number == EMPTY:
            return EMPTY_COLOR
        elif self.__view_board.is_variable_consistent(number):
            return self.__get_color_for(number)
        else:
            return ERROR_COLOR

    def __get_color_for(self, number):
        rgb = self.__get_rgb_color_for(number)
        return self._from_rgb(*rgb)

    def __get_rgb_color_for(self, number):
        step = 1.0 / self.dim ** 2
        rgb = COLORMAP(number * step)[:-1]
        return [int(255 * val) for val in rgb]

    @staticmethod
    def _from_rgb(r, g, b):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        # r, g, b = num >> 16, (num >> 8) & 0xFF, num & 0xFF
        return f'#{r:02x}{g:02x}{b:02x}'

    def __create_rectangle(self, x, y, bg_color):
        r = self.canvas.create_rectangle(x, y, x + SIDE, y + SIDE, fill=bg_color,
                                         tags=['numbers', self._tag(x, y)]
                                         )
        return r

    def show_solve_steps(self, steps):
        if not self.__ask_show_or_cancel():
            return
        self.__update_gui_and_wait(START_WAIT_SECONDS)
        for step in steps:
            if isinstance(step, Move):
                self.__show_move(step)
            elif isinstance(step, Swap):
                self.__show_swap(step)
            elif isinstance(step, Board):
                self.__show_board(step)

            self.__update_gui_and_wait(STEP_WAIT_SECONDS)
        if self.problem.is_correct():
            self.__win_animation()
        else:
            self.__lose_animation()
        self.__wait(END_WAIT_SECONDS)

    def __show_move(self, move: Move):
        if move.number == EMPTY:
            self.__delete_from_cell(move.x_pos, move.y_pos)
            self.__update_gui_and_wait(SHORT_STEP_WAIT_SECONDS)
            self.__refresh_neighbors_bg_color(move.x_pos, move.y_pos)
        else:
            self.__fill_cell(*move)
            self.__update_gui_and_wait(SHORT_STEP_WAIT_SECONDS)
            self.__refresh_neighbors_bg_color(move.x_pos, move.y_pos)

    def __delete_from_cell(self, i, j):
        x, y = self.__get_2d_gui_position(i, j)
        self.canvas.delete(self._tag(x, y))
        self.__view_board[i, j] = EMPTY

    def __show_swap(self, swap):
        first_cell = (swap.x_1, swap.y_1)
        second_cell = (swap.x_2, swap.y_2)

        # change color of swapped cells
        self.__flash_cell(*first_cell)
        self.__flash_cell(*second_cell)
        self.__update_gui_and_wait(STEP_WAIT_SECONDS)

        first_number = self.__view_board[first_cell]
        second_number = self.__view_board[second_cell]

        # fill swapped cells
        self.__set_cell(*first_cell, second_number)
        self.__set_cell(*second_cell, first_number)

    def __refresh_neighbors_bg_color(self, i, j):
        for neighbor in self.__view_board.neighbors_of_index(i, j):
            self.__refresh_cell_bg_color(*neighbor)

    def __set_cell(self, i, j, number):
        self.__delete_from_cell(i, j)
        self.__fill_cell(i, j, number)
        self.__update_gui_and_wait(SHORT_STEP_WAIT_SECONDS)
        self.__refresh_neighbors_bg_color(i, j)

    def __flash_cell(self, i, j, color=FLASH_COLOR):
        self.__light_cell(i, j, color)
        self.__update_gui_and_wait(STEP_WAIT_SECONDS)
        self.__refresh_cell_bg_color(i, j)

    def __refresh_cell_bg_color(self, i, j):
        self.__change_bg_color(i, j, bg_color=None)

    def __light_cell(self, i, j, color=FLASH_COLOR):
        self.__change_bg_color(i, j, bg_color=color)

    def __change_bg_color(self, i, j, bg_color):
        number = self.__view_board[i, j]
        self.__fill_cell(i, j, number, bg_color=bg_color)

    def __show_board(self, board: Board):
        self.__view_board = board
        self.__draw_puzzle()

    def __update_gui_and_wait(self, wait_duration):
        self.__update_gui()
        self.__wait(wait_duration)

    def __update_gui(self):
        self.parent.update_idletasks()
        self.parent.update()

    def __win_animation(self):
        self.__walking_flash_animation()
        self.__even_odd_flashing_animation()

    def __lose_animation(self):
        self.__light_cells(self.__all_coordinates())
        self.__update_gui_and_wait(STEP_WAIT_SECONDS)
        for i in range(self.dim):
            if i % 2 == 0:
                self.__flash_row_from_left(i)
            else:
                self.__flash_row_from_right(i)
        self.__flash_all_cells_error()

    def __flash_all_cells_error(self):
        self.__flash_cells(self.__all_coordinates(), color=ERROR_COLOR)
        self.__refresh_cells_bg_color(self.__all_coordinates())
        self.__update_gui_and_wait(STEP_WAIT_SECONDS)

    def __walking_flash_animation(self):
        for i, j in self.__all_coordinates():
            self.__flash_cell(i, j)
        self.__update_gui_and_wait(STEP_WAIT_SECONDS / self.dim)
        for i, j in reversed(self.__all_coordinates()[:-1]):
            self.__flash_cell(i, j)
        self.__update_gui_and_wait(STEP_WAIT_SECONDS / self.dim)

    def __even_odd_flashing_animation(self):
        self.__flash_all_even_cells()
        self.__flash_all_odd_cells()
        self.__flash_all_even_cells()
        self.__flash_all_odd_cells()
        self.__flash_all_even_cells()

    def __flash_all_odd_cells(self):
        self.__flash_cells([(i, j) for i, j in self.__all_coordinates() if self.__2d_to_1d_index(i, j) % 2 != 0])

    def __flash_all_even_cells(self):
        self.__flash_cells([(i, j) for i, j in self.__all_coordinates() if self.__2d_to_1d_index(i, j) % 2 == 0])

    def __2d_to_1d_index(self, i, j):
        return i * self.dim + j % self.dim

    def __flash_cells(self, cells, color=FLASH_COLOR):
        self.__light_cells(cells, color=color)
        self.__update_gui_and_wait(SHORT_STEP_WAIT_SECONDS)
        self.__refresh_cells_bg_color(cells)

    def __light_cells(self, cells, color=FLASH_COLOR):
        for cell in cells:
            self.__light_cell(*cell, color=color)

    def __refresh_cells_bg_color(self, cells):
        for cell in cells:
            self.__refresh_cell_bg_color(*cell)
        self.__update_gui_and_wait(SHORT_STEP_WAIT_SECONDS)

    def __all_coordinates(self):
        return [(i, j) for i in range(self.dim) for j in range(self.dim)]

    @staticmethod
    def __wait(duration):
        return time.sleep(duration)

    @staticmethod
    def _tag(x, y):
        return f'({x, y})'

    def __flash_row_from_left(self, i):
        for j in range(self.dim):
            self.__light_cell(i, j, color=ERROR_COLOR)
            self.__update_gui_and_wait(STEP_WAIT_SECONDS / self.dim)
            self.__light_cell(i, j)
        self.__update_gui_and_wait(STEP_WAIT_SECONDS / self.dim)

    def __flash_row_from_right(self, i):
        for j in range(self.dim - 1, -1, -1):
            self.__light_cell(i, j, color=ERROR_COLOR)
            self.__update_gui_and_wait(STEP_WAIT_SECONDS / self.dim)
            self.__light_cell(i, j)
        self.__update_gui_and_wait(STEP_WAIT_SECONDS / self.dim)

    def __ask_show_or_cancel(self):
        return messagebox.askokcancel('Show Solution?', 'Do you want to see the solution steps?')
