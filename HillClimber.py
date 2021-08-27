import random

import numpy as np
from matplotlib import pyplot as plt
from hidato_search_problem import *

THRESHOLD = 3


class HillClimber:

    def solve(self, problem: HidatoSearchProblem, random_restart_chance=0.1, success_threshold=0.25):
        current_state = problem.init_random_state()
        current_loss = problem.get_loss(current_state)

        loss = []

        while current_loss > problem.size * success_threshold:
            if len(loss) > 0 and len(loss) % 1000 == 0:
                self.plot_loss(np.array(loss) / problem.size)
            neighbor = problem.get_random_neighbor()
            neighbor_loss = problem.get_loss(neighbor)

            if current_loss > neighbor_loss:
                problem.set_current_state(neighbor)
                current_loss = neighbor_loss
                loss.append(current_loss)

            elif self._should_do_random_restart(random_restart_chance):
                current_state = problem.init_random_state()
                current_loss = problem.get_loss(current_state)
                loss.append(current_loss)

        return problem

    def plot_loss(self, loss):
        plt.scatter(np.arange(len(loss)), loss, marker=',')
        plt.plot(loss, c='r', linewidth=1, alpha=0.7)
        plt.xlabel('steps')
        plt.ylabel('loss')
        plt.title('HillClimb loss')
        min_loss = np.min(loss)
        plt.text(0.2, 0.2, f'min loss={min_loss}', fontsize=18)
        plt.plot(np.arange(len(loss)), np.ones_like(loss) * min_loss, c='k')
        # plt.savefig(f'plot_{len(loss)}_steps')
        plt.show()

    @staticmethod
    def _should_do_random_restart(random_restart_chance=0.1):
        return random.random() < random_restart_chance


