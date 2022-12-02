from day02 import solve


def test_solve():
    pairs = [('A', 'Y'), ('B', 'X'), ('C', 'Z')]
    puzzle = list(map(lambda pair: (ord(pair[0]) - ord('A'), ord(pair[1]) - ord('X')), pairs))
    assert solve(puzzle) == 12

