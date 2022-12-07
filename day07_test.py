from typing import List
from day07 import  solve01, solve02


def data() -> List[str]:
    return [
        "\n",
        "\n"
    ]


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert 0 == result


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert 0 == result
