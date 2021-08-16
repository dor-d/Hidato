from CSP import CSP

def ac3(problem: CSP, arcs):
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

    return True


def revise(problem: CSP, a, b):
    constraint_func = problem.get_binary_constraints(a, b)

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


