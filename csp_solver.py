import random
from functools import partial

from csp import CSP
from ac3 import ac3

MINIMUM_REMAINING_VALUES = "MRV"
LEAST_CONSTRAINING_VALUE = "LCV"


class CSPSolver:
    def solve(self, problem: CSP, select_variable, order_values, forward_checking):
        select_variable_func = self._variable_by_order
        if select_variable == MINIMUM_REMAINING_VALUES:
            select_variable_func = self._minimum_remaining_values

        order_values_func = self._random_values
        if order_values == LEAST_CONSTRAINING_VALUE:
            order_values_func = self._least_constraining_value

        return self._recursive_backtracking(problem, select_variable_func, order_values_func, forward_checking)

    def _recursive_backtracking(self, problem: CSP, select_variable_func, order_values_func, forward_checking):
        if problem.is_complete():
            return problem

        variable = select_variable_func(problem)
        for value in order_values_func(problem, variable):
            problem.assign(variable, value)
            if forward_checking:
                if (variable == 1):
                    arcs = [(2, 1)]
                elif (variable == problem.size):
                    arcs = [(problem.size - 1, variable)]
                else:
                    arcs = [(variable - 1, variable), (variable + 1, variable)]

                if not ac3(problem, arcs):
                    problem.delete_assignment(variable)
                    continue

            result = self._recursive_backtracking(problem, select_variable_func, order_values_func, forward_checking)
            if result is not None:
                return problem
            problem.delete_assignment(variable)
        return None

    def _variable_by_order(self, problem: CSP):
        return min(var for var in problem.get_variables() if not problem.is_assigned(var))

    def _minimum_remaining_values(self, problem: CSP):
        min_var = None
        min_value = -1

        for x in problem.get_variables():
            if not problem.is_assigned(x) and (problem.is_assigned(x - 1) or problem.is_assigned(x + 1)):
                value = len(problem.get_constraints(x))
                if min_var is None or value < min_value:
                    min_var = x
                    min_value = value
        return min_var

    def _random_values(self, problem: CSP, variable):
        values = list(problem.get_constraints(variable))
        random.shuffle(values)
        return values

    def num_constraints(self, value, problem):
        return len(problem.empty_neighbors(*value))

    def _least_constraining_value(self, problem, variable):
        problem_num_constraints = partial(self.num_constraints, problem=problem)

        return sorted(problem.get_constraints(variable), key=problem_num_constraints, reverse=True)

