from HidatoCSP import HidatoCSP


def ac3(problem: HidatoCSP):
    arcs = [(i, i+1) for i in problem.get_variables() if i < problem.size]
    arcs.extend((i, i - 1) for i in problem.get_variables() if i > 1)
    queue = arcs.copy()

    while queue:
        a, b = queue.pop(0)
        revised = revise(problem, a, b)

        if revised:
            if len(problem.get_domain(a)) == 0:
                return False

            #neighbors = filter(lambda arc: arc[0] != b and arc[1] == a, arcs)
            neighbors = [(neighbor, z) for (neighbor, z) in arcs if z == a]
            print(f"neighbor of {a} {neighbors}")
            queue.extend(neighbors)

    return True

def revise(problem, a, b):
    constraint_func = problem.get_constraints_2(a, b)

    a_domain = list(problem.get_domain(a))
    b_domain = list(problem.get_domain(b))

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



