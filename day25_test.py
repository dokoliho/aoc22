from typing import List
from day25 import solve01, solve02, convert, snafu_to_dec

def data() -> List[str]:
    return [
        '1=-0-2\n',
        '12111\n',
        '2=0=\n',
        '21\n',
        '2=01\n',
        '111\n',
        '20012\n',
        '112\n',
        '1=-1=\n',
        '1-12\n',
        '12\n',
        '1=\n',
        '122\n',
    ]


def test_snafu_to_def():
    lines = data()
    lines = convert(lines)
    snafus = list(map(lambda l: snafu_to_dec(l), lines))
    assert snafus == [1747, 906, 198, 11, 201, 31, 1257, 32, 353, 107, 7, 3, 37]

def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 0


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 0


