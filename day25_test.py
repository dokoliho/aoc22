from typing import List
from day25 import solve01, solve02, convert

def data() -> List[str]:
    return [
        '#.######\n',
        '#>>.<^<#\n',
        '#.<..<<#\n',
        '#>v.><>#\n',
        '#<^v^^>#\n',
        '######.#\n',
    ]


def test_convert():
    lines = data()


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 0


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 0


