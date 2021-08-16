from csp import CSP


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

    def get_binary_constraints(self, x, y):
        return self.constraints[(x, y)]



arcs = [('a', 'b'), ('b', 'a'), ('b', 'c'), ('c', 'b'), ('c', 'a'), ('a', 'c')]
print(ac3(CSPPlus(), arcs))
