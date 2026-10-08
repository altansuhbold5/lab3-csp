def solve(n):
    board = [-1] * n

    def backtrack(row):
        if row == n:
            return True

        for col in range(n):
            ok = True

            for r in range(row):
                if board[r] == col or abs(board[r] - col) == abs(r - row):
                    ok = False
                    break

            if ok:
                board[row] = col

                if backtrack(row + 1):
                    return True

                board[row] = -1

        return False

    if backtrack(0):
        for row in range(n):
            print(" ".join("Q" if board[row] == col else "." for col in range(n)))


n = int(input("N = "))
solve(n)