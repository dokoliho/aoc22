from typing import List
from day16 import solve01, solve02


def data() -> List[str]:
    return [
        '498,4 -> 498,6 -> 496,6\n',
        '503,4 -> 502,4 -> 502,9 -> 494,9\n',
     ]


def test_convert():
    pass



def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 0


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 0
