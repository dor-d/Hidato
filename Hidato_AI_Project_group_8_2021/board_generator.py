import os
import random
import subprocess

from utils import EMPTY


class HidatoGenerator:
    """
    Generate an Hidato grid with the given dimensions.
    """

    def generate_grid(self, width, height, alpha=0.5):
        grid = self._generate_puzzle_c(width, height)
        return self.omit_from_grid(width * height, grid, alpha=alpha)

    def _generate_puzzle_c(self, width, height):
        name = "./generator"
        if os.name == 'nt':
            name = "./generator.exe"
        result = subprocess.run([name, str(width), str(height)], input=None, capture_output=True, encoding='ascii',
                                text=True)
        stdout = result.stdout.rstrip(",")
        grid = [int(i) for i in stdout.split(",")]
        return grid

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
