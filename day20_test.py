from typing import List
from day20 import solve01, solve02, convert, do_all_movements


def data() -> List[str]:
    return [
        '1\n',
        '2\n',
        '-3\n',
        '3\n',
        '-2\n',
        '0\n',
        '4\n',
    ]


def test_convert():
    lines = data()
    nums = convert(lines)
    assert len(nums) == 7
    assert nums[-1] == 4


def test_do_all_movements():
    lines = data()
    nums = convert(lines)
    nums = do_all_movements(nums)
    assert nums == [1, 2, -3, 4, 0, 3, -2]


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 3


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 1623178306


