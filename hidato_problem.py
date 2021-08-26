from utils import EMPTY


class HidatoProblem:
    def __init__(self, width, height, grid):
        self.width = width
        self.height = height
        self.size = len(grid)
        self.grid = grid

    def get(self, x, y):
        raise NotImplementedError()

    def _2d_index(self, variable):
        raise NotImplementedError()

    def display(self):
        for x in range(self.width):
            print((''.join(['+'] + ['--+' for _ in range(self.height)])))
            row = ['|']
            for y in range(self.height):
                val = self.get(x, y)
                if val == EMPTY:
                    row.append('* |')
                else:
                    row.append('%2d|' % val)
            print((''.join(row)))
        print((''.join(['+'] + ['--+' for _ in range(self.height)])))

    def is_assigned(self, x):
        return x in self.grid

    def is_complete(self):
        return EMPTY not in self.grid

    def is_correct(self):
        return self.is_complete() and self.is_consistent()

    def is_consistent(self):
        prev_x, prev_y = self._2d_index(1)

        for i in range(2, self.size + 1):
            x, y = self._2d_index(i)
            if not self._are_attached(x, y, prev_x, prev_y):
                return False

            prev_x, prev_y = x, y
        return True

    def is_variable_consistent(self, variable):
        is_not_consistent = True
        x_0, y_0 = self._2d_index(variable)

        if variable == 1 and self.is_assigned(2):
            x_i, y_i = self._2d_index(2)
            is_not_consistent = self._are_attached(x_0, y_0, x_i, y_i)

        elif variable == self.size and self.is_assigned(variable - 1):
            x_i, y_i = self._2d_index(self.size - 1)
            is_not_consistent = self._are_attached(x_0, y_0, x_i, y_i)

        elif self.is_assigned(variable - 1) and self.is_assigned(variable + 1):
            x_i, y_i = self._2d_index(variable + 1)
            x_j, y_j = self._2d_index(variable - 1)
            is_not_consistent = self._are_attached(x_0, y_0, x_i, y_i) and self._are_attached(x_0, y_0, x_j, y_j)

        return is_not_consistent

    @staticmethod
    def _are_attached(x1, y1, x2, y2):
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1 and (x1 != x2 or y1 != y2)

