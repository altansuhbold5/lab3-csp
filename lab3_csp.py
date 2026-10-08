class TooSlow(Exception):
    pass


class CSP:
    def __init__(self, variables, domains, neighbors, constraint):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraint = constraint
        self.nodes = 0

    def is_consistent(self, var, value, assignment):
        for n in self.neighbors[var]:
            if n in assignment and not self.constraint(var, value, n, assignment[n]):
                return False
        return True

    def unassigned(self, assignment):
        return [v for v in self.variables if v not in assignment]


def make_map_csp(colors=("red", "green", "blue")):
    variables = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
    edges = [("WA", "NT"), ("WA", "SA"), ("NT", "SA"), ("NT", "Q"), ("SA", "Q"),
             ("SA", "NSW"), ("SA", "V"), ("Q", "NSW"), ("NSW", "V")]
    domains = {v: list(colors) for v in variables}
    neighbors = {v: [] for v in variables}
    for a, b in edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
    return CSP(variables, domains, neighbors, lambda A, a, B, b: a != b)


def make_queens_csp(n):
    variables = list(range(n))
    domains = {r: list(range(n)) for r in variables}
    neighbors = {r: [x for x in variables if x != r] for r in variables}

    def constraint(A, a, B, b):
        return a != b and abs(a - b) != abs(A - B)

    return CSP(variables, domains, neighbors, constraint)


def print_board(assignment, n):
    for r in range(n):
        print(" ".join("Q" if assignment[r] == c else "." for c in range(n)))


def legal_values(csp, var, assignment):
    return [x for x in csp.domains[var] if csp.is_consistent(var, x, assignment)]


def select_unassigned_variable(csp, assignment, use_mrv=True, use_degree=True):
    free = csp.unassigned(assignment)
    if not use_mrv:
        return free[0]

    def legal(v):
        return len(legal_values(csp, v, assignment))

    def degree(v):
        return sum(1 for n in csp.neighbors[v] if n not in assignment)

    if use_degree:
        return min(free, key=lambda v: (legal(v), -degree(v)))
    return min(free, key=legal)


def order_domain_values(csp, var, assignment, use_lcv=True):
    values = legal_values(csp, var, assignment)
    if not use_lcv:
        return values

    def removed(x):
        total = 0
        for n in csp.neighbors[var]:
            if n in assignment:
                continue
            for y in legal_values(csp, n, assignment):
                if not csp.constraint(var, x, n, y):
                    total += 1
        return total

    return sorted(values, key=removed)


def backtrack(csp, assignment, use_mrv=False, use_degree=False,
              use_lcv=False, limit=None):
    if len(assignment) == len(csp.variables):
        return dict(assignment)

    var = select_unassigned_variable(csp, assignment, use_mrv, use_degree)
    for value in order_domain_values(csp, var, assignment, use_lcv):
        csp.nodes += 1
        if limit and csp.nodes > limit:
            raise TooSlow
        assignment[var] = value
        result = backtrack(csp, assignment, use_mrv, use_degree, use_lcv, limit)
        if result is not None:
            return result
        del assignment[var]
    return None


def backtracking_search(csp, **options):
    csp.nodes = 0
    return backtrack(csp, {}, **options)


def check_solution(csp, assignment):
    if assignment is None or set(assignment) != set(csp.variables):
        return False
    for a in csp.variables:
        for b in csp.neighbors[a]:
            if not csp.constraint(a, assignment[a], b, assignment[b]):
                return False
    return True


def count_solutions(csp, use_mrv=False, use_degree=False, use_lcv=False):
    csp.nodes = 0

    def rec(assignment):
        if len(assignment) == len(csp.variables):
            return 1
        var = select_unassigned_variable(csp, assignment, use_mrv, use_degree)
        total = 0
        for value in order_domain_values(csp, var, assignment, use_lcv):
            csp.nodes += 1
            assignment[var] = value
            total += rec(assignment)
            del assignment[var]
        return total

    return rec({})


CONFIGS = {
    "A. Heuristic-гүй":      dict(use_mrv=False, use_degree=False, use_lcv=False),
    "B. MRV":                dict(use_mrv=True,  use_degree=False, use_lcv=False),
    "C. MRV + Degree":       dict(use_mrv=True,  use_degree=True,  use_lcv=False),
    "D. MRV + Degree + LCV": dict(use_mrv=True,  use_degree=True,  use_lcv=True),
}
LIMIT = 1_000_000


def run(make_csp, options):
    csp = make_csp()
    try:
        solution = backtracking_search(csp, limit=LIMIT, **options)
    except TooSlow:
        return "хэт удаан"
    assert check_solution(csp, solution)
    return csp.nodes


def compare():
    problems = {
        "Газрын зураг": make_map_csp,
        "8-Queens": lambda: make_queens_csp(8),
        "12-Queens": lambda: make_queens_csp(12),
        "16-Queens": lambda: make_queens_csp(16),
    }
    table = {}
    for name, opts in CONFIGS.items():
        table[name] = [run(mk, opts) for mk in problems.values()]
    return list(problems), table


if __name__ == "__main__":
    c = make_map_csp()
    print("is_consistent:", c.is_consistent("NT", "red", {"WA": "red"}),
          c.is_consistent("NT", "green", {"WA": "red"}))
    print("хөршийн тоо SA/T/WA:", len(c.neighbors["SA"]), len(c.neighbors["T"]),
          len(c.neighbors["WA"]))
    s = backtracking_search(c)
    print("газрын зураг:", s, check_solution(c, s), "зангилаа:", c.nodes)
    print("шийдийн тоо:", [count_solutions(make_queens_csp(n)) for n in range(1, 9)])
    q = make_queens_csp(4)
    print_board(backtracking_search(q), 4)
    print("MRV:", select_unassigned_variable(make_map_csp(), {"WA": "red"}, True, False))
    print("Degree:", select_unassigned_variable(make_map_csp(), {}, True, True))
    print("LCV:", order_domain_values(make_map_csp(), "Q", {"WA": "red", "NT": "green"}))
    print("MRV-тэй 8-Queens:", count_solutions(make_queens_csp(8), use_mrv=True))
    cols, tab = compare()
    for k, v in tab.items():
        print(k, v)