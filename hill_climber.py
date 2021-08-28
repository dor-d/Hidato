import math
import random
from math import ceil

import numpy as np
from matplotlib import pyplot as plt
# import simpleai

from hidato_search_problem import HidatoSearchProblem


class HillClimber:
    """
    Solve Hidato with stochastic hill-climbing with random-restarts.
    """

    def solve(self, problem: HidatoSearchProblem, max_steps=math.inf):

        loss = []

        problem.init_random_state()

        best_state = None
        best_loss = 0

        steps = 0

        while steps <= max_steps:
            steps += 1
            current_loss = problem.get_current_loss()

            if current_loss == 0:
                break

            loss.append(current_loss)

            if best_state is None or current_loss < best_loss:
                best_state, best_loss = problem.get_current_state(), problem.get_current_loss()

            found_better_neighbor = problem.move_to_first_better_neighbor()

            if not found_better_neighbor:
                problem.init_random_state()

        current_loss = problem.get_current_loss()
        loss.append(current_loss)
        if current_loss < best_loss:
            best_state = problem.get_current_state()

        problem.set_current_state(best_state)
        self.plot_loss(loss)
        return problem

        # if expander == "first-choice":
        #     neighbor = problem.get_random_neighbor()
        # else:
        #     neighbor = problem.move_to_best_neighbor()

        # neighbor_loss = problem.get_loss(neighbor)

        # if current_loss <= neighbor_loss:
        #     problem.undo_last_move()
        #
        #     if self._should_do_random_restart(random_restart_chance):
        #         random_state = problem.get_random_state()
        #         random_state_loss = problem.get_loss(random_state)
        #
        #         if random_state_loss < current_loss:
        #             problem.set_current_state(random_state)
        #             current_state, current_loss = random_state, random_state_loss
        #         else:
        #             problem.undo_last_move()
        #
        # elif neighbor_loss < current_loss:
        #     problem.set_current_state(neighbor)
        #     current_state, current_loss = neighbor, neighbor_loss
        #
        # if best_state is None or current_loss < best_loss:
        #     best_loss, best_state = current_loss, current_state

        # problem.set_current_state(best_state)

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
