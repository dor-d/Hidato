from tkinter import Canvas, Frame, BOTH, TOP, Tk
from hidato_csp import Move
from utils import EMPTY
import time

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
STEP_TIME = 0.3


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
        step = int((color_end - color_start) / self.dim**2)
        other_color = 0

        current_color = color_start
        for i in range(1, self.dim**2 + 1):
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
                    x = self.get_gui_position(j)
                    y = self.get_gui_position(i)
                    self.fill_cell(number, 'black', x, y)

    @staticmethod
    def get_gui_position(j):
        return MARGIN + j * SIDE

    def fill_cell(self, number, color, x, y):
        z=self.canvas.create_text(
            x + SIDE / 2, y + SIDE / 2, text=number, tags=["numbers", self._tag(x, y)], fill=color
        )
        r = self.canvas.create_rectangle(x, y, x + SIDE, y + SIDE, fill=self.colors[number - 1],
                                         tags=[self._tag(x, y)])

        self.canvas.tag_lower(r, z)

    def make_moves(self, moves):
        for move in moves:
            self.make_move(move)
            self.update_parent()
            time.sleep(STEP_TIME)

    def update_parent(self):
        self.parent.update_idletasks()
        self.parent.update()

    def make_move(self, move: Move):
        i, j = move.index // self.dim, move.index % self.dim
        x = self.get_gui_position(j)
        y = self.get_gui_position(i)
        if move.number == EMPTY:
            self.delete_from_cell(x, y)
        else:
            self.fill_cell(move.number, 'black', x, y)

    def delete_from_cell(self, x, y):
        self.canvas.delete(self._tag(x, y))

    def _tag(self, x, y):
        return f'({x, y})'
