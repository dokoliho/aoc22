from typing import List
from day18 import solve01, solve02


def data() -> List[str]:
    return [
        '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>\n',
    ]


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 0


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 0
