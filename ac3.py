from CSP import CSP

class CSPPlus(CSP):
    def __init__(self):
        self.domains = {
            'a': [2, 3, 4, 5, 6, 7],
            'b': [4, 5, 6, 7, 8, 9],
            'c': [1, 2, 3, 4, 5]
        }

        self.constraints = {
            ('a', 'b'): lambda a, b: a * 2 == b,
            ('b', 'a'): lambda b, a: b == 2 * a,
            ('a', 'c'): lambda a, c: a == c,
            ('c', 'a'): lambda c, a: c == a,
            ('b', 'c'): lambda b, c: b >= c - 2,
            ('b', 'c'): lambda b, c: b <= c + 2,
            ('c', 'b'): lambda c, b: b >= c - 2,
            ('c', 'b'): lambda c, b: b <= c + 2
        }

    def get_variables(self):
        return list(self.domains.keys())

    def get_domain(self, variable):
        return self.domains[variable]

    def get_constraints_between(self, x, y):
        return self.constraints[(x, y)]


def ac3(problem, arcs):
    queue = arcs.copy()

    while queue:
        x, y = queue.pop(0)

        if revise(problem, x, y):
            if len(problem.get_domain(x)) == 0:
                # inconsistency was found
                return False

            neighbors = set()
            for arc in arcs:
                if arc[0] == x and arc[1] != y:
                    neighbors.add((arc[1], x))
                elif arc[1] == x and arc[0] != y:
                    neighbors.add((arc[0], x))

            queue.extend(neighbors)

    return True, problem.domains

def revise(problem, a, b):
    constraint_func = problem.get_constraints_between(a, b)

    a_domain = problem.get_domain(a).copy()
    b_domain = problem.get_domain(b).copy()

    revised = False

    for a_value in a_domain:
        satisfies = False
        for b_value in b_domain:
            if constraint_func(a_value, b_value):
                satisfies = True

        if not satisfies:
            problem.get_domain(a).remove(a_value)
            revised = True

    return revised


arcs = [('a', 'b'), ('b', 'a'), ('b', 'c'), ('c', 'b'), ('c', 'a'), ('a', 'c')]
print(ac3(CSPPlus(), arcs))

