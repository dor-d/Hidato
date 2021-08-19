import random

from HidatoSearchProblem import *

THRESHOLD = 0


class HillClimber:

    def solve(self, problem: HidatoSearchProblem, random_restart_chance=0.1):
        current_state = problem.init_random_state()
        current_loss = problem.get_loss(current_state)

        while current_loss > THRESHOLD:

            neighbor = problem.get_random_neighbor()
            neighbor_loss = problem.get_loss(neighbor)

            if current_loss > neighbor_loss:
                problem.set_current_state(neighbor)
                current_loss = neighbor_loss

            elif self._should_do_random_restart(random_restart_chance):
                current_state = problem.init_random_state()
                current_loss = problem.get_loss(current_state)

        return problem

    @staticmethod
    def _should_do_random_restart(random_restart_chance=0.1):
        return random.random() < random_restart_chance
