import functools

import CSP
from functools import partial


class SolverCSP:

    def solve(self, problem: CSP):
        return self._recursive_backtracing(problem)

    def _recursive_backtracing(self, problem: CSP):
        if problem.is_complete():
            return problem

        x = self._minimum_remaining_values(problem)
        problem_num_constraints = partial(self.num_constraints, problem=problem)
        for value in sorted(problem.get_constraints(x), key=problem_num_constraints, reverse=True):
            problem.assign(x, value)
            result = self._recursive_backtracing(problem)
            if result is not None:
                return problem
            problem.delete_assignment(x)
        return None

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

    def num_constraints(self, value, problem):
        return len(problem.empty_neighbors(*value))
