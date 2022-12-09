from typing import List
from day09 import solve01, solve02, convert


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


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 0


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 0
