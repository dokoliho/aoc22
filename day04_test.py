from day04 import convert_to_tuples, is_containing, solve01, is_overlapping, solve02


def data():
    return ["2-4,6-8\n", "2-3,4-5\n", "5-7,7-9\n", "2-8,3-7\n", "6-6,4-6\n", "2-6,4-8\n"]


def test_convert_to_tuples():
    lines = data()
    result = convert_to_tuples(lines)
    assert result == [[(2, 4), (6, 8)], [(2, 3), (4, 5)], [(5, 7), (7, 9)],
                      [(2, 8), (3, 7)], [(6, 6), (4, 6)], [(2, 6), (4, 8)]]


def test_is_containing():
    assert is_containing((3, 5), (4, 4))
    assert is_containing((4, 5), (2, 7))
    assert not(is_containing((4, 5), (8, 10)))


def test_is_overlapping():
    assert is_overlapping((3, 5), (5, 8))
    assert is_overlapping((1, 10), (2, 4))
    assert is_overlapping((1, 5), (4, 7))
    assert not(is_overlapping((1, 5), (6, 7)))


def test_solve1():
    lines = data()
    puzzle = convert_to_tuples(lines)
    assert 2 == solve01(puzzle)

def test_solve2():
    lines = data()
    puzzle = convert_to_tuples(lines)
    assert 4 == solve02(puzzle)
