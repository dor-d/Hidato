import random
from math import ceil

from hidato_search_problem import HidatoSearchProblem


class HillClimber:
    """
    Solve Hidato with stochastic hill-climbing with random-restarts.
    """

    def solve(self, problem: HidatoSearchProblem, max_iterations=None, random_restart_chance=0.005):
        if max_iterations is None:
            max_iterations = ceil(problem.size ** 0.5 * 5000)

        current_state = problem.init_random_state()
        current_loss = problem.get_loss(current_state)

        best_state = None
        best_loss = 0

        for i in range(max_iterations):
            neighbor = problem.get_random_neighbor()
            neighbor_loss = problem.get_loss(neighbor)

            if current_loss <= neighbor_loss:
                problem.pop_swap_from_moves()

                if self._should_do_random_restart(random_restart_chance):
                    current_state = problem.init_random_state()
                    current_loss = problem.get_loss(current_state)

            elif current_loss > neighbor_loss:
                problem.set_current_state(neighbor)
                current_loss = neighbor_loss

            if best_state is None or current_loss < best_loss:
                best_loss = current_loss
                best_state = current_state

        problem.set_current_state(best_state)

        return problem

    @staticmethod
    def _should_do_random_restart(random_restart_chance=0.1):
        return random.random() < random_restart_chance
