from typing import List
from day09 import solve01, solve02, convert, new_tail_after_close_gap, tail_positions_after_movement


def data() -> List[str]:
    return [
        "R 4\n",
        "U 4\n",
        "L 3\n",
        "D 1\n",
        "R 4\n",
        "D 1\n",
        "L 5\n",
        "R 2\n",
    ]

def test_convert():
    lines = data()
    result = convert(lines)
    assert result[0] == ('R', 4)
    assert len(result) == 8


def test_new_tail_after_close_gap():
    head = (0,0)
    tail = (0,0)
    new_tail = new_tail_after_close_gap(head, tail)
    assert new_tail == (0, 0)

    head = (0,1)
    tail = (0,0)
    new_tail = new_tail_after_close_gap(head, tail)
    assert new_tail == (0, 0)

    head = (0,2)
    tail = (0,0)
    new_tail = new_tail_after_close_gap(head, tail)
    assert new_tail == (0, 1)

    head = (-2,0)
    tail = (0,0)
    new_tail = new_tail_after_close_gap(head, tail)
    assert new_tail == (-1, 0)

    head = (1,-1)
    tail = (0,0)
    new_tail = new_tail_after_close_gap(head, tail)
    assert new_tail == (0, 0)

    head = (1,-2)
    tail = (0,0)
    new_tail = new_tail_after_close_gap(head, tail)
    assert new_tail == (1, -1)


def test_tail_positions_after_movement():
    head = (0, 0)
    tail = (0, 0)
    result, _, _ = tail_positions_after_movement(head, tail, 'R', 3)
    assert result == [(0,0), (0,0), (1,0), (2,0)]


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 13


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 0
