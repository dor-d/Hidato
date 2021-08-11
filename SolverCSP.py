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
        return self._argmin(lambda var: len(problem.get_constraints(var)),
                            problem.get_variables(),
                            lambda var: not problem.is_assigned(var) and (
                                    problem.is_assigned(var - 1) or problem.is_assigned(var + 1))
                            )

    def num_constraints(self, value, problem):
        return len(problem.empty_neighbors(*value))

    def _argmin(self, func, args, filter_func):
        min_arg = None
        min_value = -1

        for arg in args:
            if filter_func(arg):
                value = func(arg)
                if min_arg is None or value < min_value:
                    min_arg = arg
                    min_value = value
        return min_arg
