from typing import List
from day11 import solve01, solve02, convert


def data() -> List[str]:
    return [
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
