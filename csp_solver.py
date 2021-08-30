import random
from collections import defaultdict

from hidato_csp import HidatoCSP

MINIMUM_REMAINING_VALUES = "MRV"
LEAST_CONSTRAINING_VALUE = "LCV"


class CSPSolver:
    def __init__(self, problem: HidatoCSP):
        self.problem = problem
        self._num_of_iterations = 0

    def solve(self, select_variable, order_values, forward_checking):
        select_variable_func = self._variable_by_order
        if select_variable == MINIMUM_REMAINING_VALUES:
            select_variable_func = self._minimum_remaining_values

        order_values_func = self._random_values
        if order_values == LEAST_CONSTRAINING_VALUE:
            order_values_func = self._least_constraining_value

        self._num_of_iterations = 0
        result = self._recursive_backtracking(select_variable_func, order_values_func, forward_checking)
        if self._num_of_iterations == 0:
            self.problem.display()
            print(select_variable, order_values, forward_checking)
        return result

    def _recursive_backtracking(self, select_variable_func, order_values_func, forward_checking):
        if self.problem.is_correct():
            return self.problem

        variable = select_variable_func()
        if variable is None:
            return
        for value in order_values_func(variable):
            old_domains = self.problem.get_domains_copy()
            self._num_of_iterations += 1
            self.problem.assign(variable, value)

            if forward_checking:
                arcs = self.problem.get_arcs(variable)

                if not self.ac3(arcs.copy()):
                    self.problem.delete_assignment(variable, old_domains)
                    continue

            result = self._recursive_backtracking(select_variable_func, order_values_func,
                                                  forward_checking)

            if result is not None:
                return self.problem

            self.problem.delete_assignment(variable, old_domains)

        return

    def _variable_by_order(self):
        return min(var for var in self.problem.get_variables() if not self.problem.board.is_assigned(var))

    def _minimum_remaining_values(self):
        def domain_size(var):
            return len(self.problem.domains[var])

        sorted_variables = sorted(self.problem.get_unassigned_variables(), key=domain_size)

        return sorted_variables[0] if len(sorted_variables) > 0 else None

    @staticmethod
    def _random_values(variable, domains):
        values = list(domains[variable])
        random.shuffle(values)
        return values

    def _least_constraining_value(self, variable):
        occurrences = defaultdict(int)
        for x in self.problem.get_unassigned_variables():
            for val in self.problem.domains[x]:
                occurrences[val] += 1

        return sorted(self.problem.domains[variable], key=lambda a: occurrences[a])

    def ac3(self, arcs_queue):
        while arcs_queue:
            y, x = arcs_queue.pop(0)

            if self.revise(y, x):
                if len(self.problem.domains[x]) == 0:
                    # inconsistency was found
                    return False

                neighbors = set()
                for arc in arcs_queue:
                    if arc[0] == x and arc[1] != y:
                        neighbors.add((arc[1], x))
                    elif arc[1] == x and arc[0] != y:
                        neighbors.add((arc[0], x))

                arcs_queue.extend(neighbors)

        return True

    def revise(self, a, b):
        constraint_func = self.problem.get_binary_constraints(a, b)

        revised = False

        for a_value in self.problem.domains[a]:
            satisfies = False
            for b_value in self.problem.domains[b]:
                if constraint_func(a_value, b_value):
                    satisfies = True

            if not satisfies:
                self.problem.domains[a].remove(a_value)
                revised = True

        return revised
