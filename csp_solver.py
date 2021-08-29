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
        domains = self.problem.get_domains()
        result = self._recursive_backtracking(domains, select_variable_func, order_values_func, forward_checking)
        if self._num_of_iterations == 0:
            self.problem.display()
            print(select_variable, order_values, forward_checking)
        return result

    def _recursive_backtracking(self, domains, select_variable_func, order_values_func, forward_checking):
        if self.problem.is_complete():
            return self.problem

        variable = select_variable_func(domains)
        for value in order_values_func(variable, domains):
            self._num_of_iterations += 1

            self.problem.assign(variable, value)
            if forward_checking:
                arcs = self.problem.get_arcs(variable)

                if not self.ac3(arcs):
                    self.problem.delete_assignment(variable)
                    continue

            result = self._recursive_backtracking(domains, select_variable_func, order_values_func, forward_checking)
            if result is not None:
                return self.problem

            self.problem.delete_assignment(variable)

        return

    def _variable_by_order(self, domains):
        return min(var for var in self.problem.get_variables() if not self.problem.board.is_assigned(var))

    def _minimum_remaining_values(self, domains):
        def domain_size(var):
            return len(domains[var])

        return sorted(self.problem.get_variables(), key=domain_size)[0]

    @staticmethod
    def _random_values(variable, domains):
        values = list(domains[variable])
        random.shuffle(values)
        return values

    def _least_constraining_value(self, variable, domains):
        occurrences = defaultdict(int)
        for x in self.problem.get_unassigned_variables():
            for val in domains[x]:
                occurrences[val] += 1

        return sorted(domains[variable], key=lambda a: occurrences[a])

    def ac3(self, arcs, domains):
        queue = arcs.copy()

        while queue:
            y, x = queue.pop(0)

            if self.revise(y, x, domains):
                if len(self.problem.get_domain(x)) == 0:
                    # inconsistency was found
                    return False

                neighbors = set()
                for arc in arcs:
                    if arc[0] == x and arc[1] != y:
                        neighbors.add((arc[1], x))
                    elif arc[1] == x and arc[0] != y:
                        neighbors.add((arc[0], x))

                queue.extend(neighbors)

        return True

    def revise(self, a, b, domains):
        constraint_func = self.problem.get_binary_constraints(a, b)

        a_domain = self.problem.get_constraints(a)
        b_domain = self.problem.get_constraints(b)

        revised = False

        for a_value in a_domain:
            satisfies = False
            for b_value in b_domain:
                if constraint_func(a_value, b_value):
                    satisfies = True

            if not satisfies:
                revised = True

        return revised
