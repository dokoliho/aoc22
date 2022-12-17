from typing import List
from day17 import solve01, solve02


def data() -> List[str]:
    return [
        '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>\n',
    ]


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 3068


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 1514285714288
