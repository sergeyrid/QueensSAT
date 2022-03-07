from pysat.formula import CNF
from pysat.solvers import Minisat22


def get_index(n: int, i: int, j: int) -> int:
    return i * n + j + 1


def main():
    n = 3
    clauses = CNF()
    for i in range(n):
        row_min_clause = []
        col_min_clause = []
        for j in range(n):
            row_min_clause.append(get_index(n, i, j))  # at least 1 queen in a row
            col_min_clause.append(get_index(n, j, i))  # at least 1 queen in a column
            for k in range(j):
                row_max_clause = [-get_index(n, i, j), -get_index(n, i, k)]  # at most 1 queen in a row
                clauses.append(row_max_clause)
        clauses.append(row_min_clause)
        clauses.append(col_min_clause)
    for i in range(n):
        for j in range(n):
            cur_index = get_index(n, i, j)
            for k in range(1, n):  # at most 1 queen in a diagonal
                if i - k >= 0 and j - k >= 0:
                    diag_clause = [-cur_index, -get_index(n, i - k, j - k)]
                    clauses.append(diag_clause)
                if i + k < n and j - k >= 0:
                    diag_clause = [-cur_index, -get_index(n, i + k, j - k)]
                    clauses.append(diag_clause)
                if i - k >= 0 and j + k < n:
                    diag_clause = [-cur_index, -get_index(n, i - k, j + k)]
                    clauses.append(diag_clause)
                if i + k < n and j + k < n:
                    diag_clause = [-cur_index, -get_index(n, i + k, j + k)]
                    clauses.append(diag_clause)
    with Minisat22(bootstrap_with=clauses) as solver:
        solved = solver.solve()
        if solved:
            model = solver.get_model()
            for i in range(n):
                for j in range(n):
                    if model[get_index(n, i, j) - 1] > 0:
                        print('X', end='')
                    else:
                        print('_', end='')
                print()
        else:
            print('IMPOSSIBLE')


if __name__ == '__main__':
    main()
