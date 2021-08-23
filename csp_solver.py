import random

MINIMUM_REMAINING_VALUES = "MRV"
LEAST_CONSTRAINING_VALUE = "LCV"



class CSPSolver:
    def __init__(self, problem):
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
        if self.problem.is_complete():
            return self.problem

        variable = select_variable_func()
        for value in order_values_func(variable):
            self._num_of_iterations += 1

            self.problem.assign(variable, value)
            if forward_checking:
                arcs = self.problem.get_arcs(variable)

                if not self.ac3(arcs):
                    self.problem.delete_assignment(variable)
                    continue

            result = self._recursive_backtracking(select_variable_func, order_values_func, forward_checking)
            if result is not None:
                return self.problem
            self.problem.delete_assignment(variable)

        return

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

    def ac3(self, arcs):
        queue = arcs.copy()

        while queue:
            x, y = queue.pop(0)

            if self.revise(x, y):
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

    def revise(self, a, b):
        constraint_func = self.problem.get_binary_constraints(a, b)

        a_domain = self.problem.get_domain(a).copy()
        b_domain = self.problem.get_domain(b).copy()

        revised = False

        for a_value in a_domain:
            satisfies = False
            for b_value in b_domain:
                if constraint_func(a_value, b_value):
                    satisfies = True

            if not satisfies:
                self.problem.get_domain(a).remove(a_value)
                revised = True

        return revised
