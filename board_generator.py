import anneal
import random
from hidato_csp import *


class HidatoGenerator:

    def generate_hidato(self, width, height, alpha=0.5):
        grid = self.generate_puzzle(width, height)
        grid = self.omit_from_grid(width * height, grid, alpha=alpha)
        return HidatoCSP(width, height, grid)

    def generate_puzzle(self, width, height):
        def energy(state):
            return state.energy()

        def do_move(state):
            return state.do_move()

        def undo_move(state, undo_data):
            state.undo_move(undo_data)

        def make_copy(state):
            result = Model(state.width, state.height, False)
            result.end = state.end
            result.next = list(state.next)
            return result

        e = True
        while e:
            state = Model(width, height)
            annealer = anneal.Annealer(energy, do_move, undo_move, make_copy)
            state, e = annealer.anneal(state, width * height, 0.1, 100000)
        return state.get_grid()

    def omit_from_grid(self, size, grid, alpha=0.5):
        numbers = [i for i in range(size)]
        to_remove = self.choices(numbers, k=int(alpha * size))
        for i in numbers:
            if i in to_remove:
                grid[i] = EMPTY
        return grid

    def choices(self, population, k=1):
        random.shuffle(population)
        return population[:k]


class Model(object):
    def __init__(self, width, height, _reset=True):
        self.width = width
        self.height = height
        self.size = width * height
        if _reset:
            self.reset()

    def reset(self):
        self.end = random.randint(0, self.size - 1)
        self.next = [-1] * self.size
        for i in range(self.size):
            if i == self.end:
                continue
            self.next[i] = self.random_neighbor(self.width, self.height, i)

    def energy(self):
        return self.get_grid().count(-1)

    def do_move(self):
        while True:
            i = random.randint(0, self.size - 1)
            if i == self.end:
                continue
            result = (i, self.next[i])
            self.next[i] = self.random_neighbor(self.width, self.height, i)
            return result

    def undo_move(self, xxx_todo_changeme):
        (index, value) = xxx_todo_changeme
        self.next[index] = value

    def get_grid(self):
        result = [-1] * self.size
        lookup = {self.next[i]: i for i in range(self.size)}
        index = self.end
        number = self.size
        for _ in range(self.size):
            result[index] = number
            number -= 1
            if index not in lookup:
                break
            index = lookup[index]
        return result

    def compute_neighbors(self, width, height):
        neighbors = {}
        for y in range(height):
            for x in range(width):
                i = y * width + x
                neighbors[i] = []
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if nx == x and ny == y:
                            continue
                        if nx < 0 or nx >= width:
                            continue
                        if ny < 0 or ny >= height:
                            continue
                        j = ny * width + nx
                        neighbors[i].append(j)
        return neighbors

    def random_neighbor(self, width, height, index, cache={}):
        key = (width, height)
        if key not in cache:
            cache[key] = self.compute_neighbors(width, height)
        neighbors = cache[key]
        return random.choice(neighbors[index])
