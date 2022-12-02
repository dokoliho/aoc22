from day02 import solve, draw_lost_won


def test_solve():
    pairs = [('A', 'Y'), ('B', 'X'), ('C', 'Z')]
    puzzle = list(map(lambda pair: (ord(pair[0]) - ord('A'), ord(pair[1]) - ord('X')), pairs))
    assert solve(puzzle) == 12

def test_draw_loss_won():
    assert draw_lost_won((0, 1)) == 2 # Papier schlägt Stein
    assert draw_lost_won((1, 0)) == 1 # Stein unterliegt Papier
    assert draw_lost_won((2, 0)) == 2 # Stein schlägt Schere
    assert draw_lost_won((2, 2)) == 0 # 2x Schere -> draw
