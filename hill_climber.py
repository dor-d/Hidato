import random

import numpy as np
from matplotlib import pyplot as plt

from hidato_search_problem import HidatoSearchProblem

RANDOM_CHOICE = "random-choice"
FIRST_CHOICE = "first-choice"


class HillClimber:
    """
    Solve Hidato with stochastic hill-climbing with random-restarts.
    """

    def solve(self, problem: HidatoSearchProblem, max_steps=None, expander=FIRST_CHOICE):

        loss = []

        best_state = None
        best_loss = 0

        if max_steps is None:
            max_steps = problem.size * 3
        steps = 0
        problem.init_random_state()

        with tqdm(total=max_steps) as pbar:
            while steps <= max_steps:
                steps += 1
                current_loss = problem.get_current_loss()

                if current_loss == 0:
                    break

                loss.append(current_loss)

                if best_state is None or current_loss < best_loss:
                    best_state, best_loss = problem.get_current_state(), problem.get_current_loss()

                if expander == RANDOM_CHOICE:
                    found_better_neighbor = problem.get_random_neighbor()
                elif expander == FIRST_CHOICE:
                    found_better_neighbor = problem.move_to_first_better_neighbor()

                if not found_better_neighbor:
                    problem.init_random_state()

                pbar.update(1)

        current_loss = problem.get_current_loss()
        loss.append(current_loss)
        if current_loss < best_loss:
            best_state = problem.get_current_state()

        problem.set_current_state(best_state)
        self.plot_loss(loss, expander)
        return problem

    @staticmethod
    def plot_loss(loss, title):
        plt.scatter(np.arange(len(loss)), loss, marker='.', color='green')
        plt.plot(loss, c='r', linewidth=1, alpha=0.7)
        plt.xlabel('steps')
        plt.ylabel('loss')
        min_loss = np.min(loss)
        plt.title(f'{title} hill-climbing loss, min loss = {"{0:.3g}".format(min_loss)}')
        plt.plot(np.arange(len(loss)), np.ones_like(loss) * min_loss, c='k')
        plt.savefig(f'hillclimb_loss_plot_{len(loss)}_steps')
        plt.show()

    @staticmethod
    def _should_do_random_restart(random_restart_chance=0.1):
        return random.random() < random_restart_chance
