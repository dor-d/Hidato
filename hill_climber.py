import random
from math import ceil

import numpy as np
from matplotlib import pyplot as plt
import simpleai

from hidato_search_problem import HidatoSearchProblem


class HillClimber:
    """
    Solve Hidato with stochastic hill-climbing with random-restarts.
    """
    def solve(self, problem: HidatoSearchProblem, max_iterations=None, random_restart_chance=0.01,
              expander="first-1choice"):

        loss = []

        if max_iterations is None:
            max_iterations = ceil(problem.size ** 0.5 * 5000)

        current_state = problem.get_random_state()
        problem.set_current_state(current_state)
        current_loss = problem.get_loss(current_state)

        best_state = None
        best_loss = 0

        for i in range(max_iterations):
            if current_loss < problem.size ** 2 * 0.01:
                break

            if len(loss) == 0 or current_loss < loss[-1]:
                loss.append(current_loss)

            if expander == "first-choice":
                neighbor = problem.get_random_neighbor()
            else:
                neighbor = problem.get_best_neighbor()

            neighbor_loss = problem.get_loss(neighbor)

            if current_loss <= neighbor_loss:
                problem.undo_last_move()

                if self._should_do_random_restart(random_restart_chance):
                    random_state = problem.get_random_state()
                    random_state_loss = problem.get_loss(random_state)

                    if random_state_loss < current_loss:
                        problem.set_current_state(random_state)
                        current_state, current_loss = random_state, random_state_loss
                    else:
                        problem.undo_last_move()

            elif neighbor_loss < current_loss:
                problem.set_current_state(neighbor)
                current_state, current_loss = neighbor, neighbor_loss

            if best_state is None or current_loss < best_loss:
                best_loss, best_state = current_loss, current_state

        problem.set_current_state(best_state)
        self.plot_loss(loss)

        return problem

    @staticmethod
    def plot_loss(loss):
        plt.scatter(np.arange(len(loss)), loss, marker='.', color='green')
        plt.plot(loss, c='r', linewidth=1, alpha=0.7)
        plt.xlabel('steps')
        plt.ylabel('loss')
        min_loss = np.min(loss)
        plt.title(f'HillClimb loss, min loss = {min_loss}')
        plt.plot(np.arange(len(loss)), np.ones_like(loss) * min_loss, c='k')
        plt.savefig(f'hillclimb_loss_plot_{len(loss)}_steps')
        plt.show()

    @staticmethod
    def _should_do_random_restart(random_restart_chance=0.1):
        return random.random() < random_restart_chance
