import random

from csp import CSP
from ac3 import ac3

MINIMUM_REMAINING_VALUES = "MRV"
LEAST_CONSTRAINING_VALUE = "LCV"


class CSPSolver:
    def __init__(self, problem: CSP):
        self.problem = problem

    def solve(self, select_variable, order_values, forward_checking):
        select_variable_func = self._variable_by_order
        if select_variable == MINIMUM_REMAINING_VALUES:
            select_variable_func = self._minimum_remaining_values

        order_values_func = self._random_values
        if order_values == LEAST_CONSTRAINING_VALUE:
            order_values_func = self._least_constraining_value

        return self._recursive_backtracking(select_variable_func, order_values_func, forward_checking)

    def _recursive_backtracking(self, select_variable_func, order_values_func, forward_checking):
        if self.problem.is_complete():
            return self.problem

        variable = select_variable_func()
        for value in order_values_func(variable):
            self.problem.assign(variable, value)
            if forward_checking:
                if variable == 1:
                    arcs = [(2, 1)]
                elif variable == self.problem.size:
                    arcs = [(self.problem.size - 1, variable)]
                else:
                    arcs = [(variable - 1, variable), (variable + 1, variable)]

                if not ac3(self.problem, arcs):
                    self.problem.delete_assignment(variable)
                    continue

            result = self._recursive_backtracking(select_variable_func, order_values_func, forward_checking)
            if result is not None:
                return self.problem
            self.problem.delete_assignment(variable)
        return None

    def _variable_by_order(self):
        return min(var for var in self.problem.get_variables() if not self.problem.is_assigned(var))

    def _minimum_remaining_values(self):
        min_var = None
        min_value = -1

        for x in self.problem.get_variables():
            if not self.problem.is_assigned(x) and (self.problem.is_assigned(x - 1) or self.problem.is_assigned(x + 1)):
                value = len(self.problem.get_constraints(x))
                if min_var is None or value < min_value:
                    min_var = x
                    min_value = value
        return min_var

    def _random_values(self, variable):
        values = list(self.problem.get_constraints(variable))
        random.shuffle(values)
        return values

    def num_constraints(self, value):
        return len(self.problem.empty_neighbors(*value))

    def _least_constraining_value(self, variable):
        return sorted(self.problem.get_constraints(variable), key=self.num_constraints, reverse=True)
