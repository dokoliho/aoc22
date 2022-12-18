from typing import List
from day18 import solve01, solve02, convert


def data() -> List[str]:
    return [
        '2,2,2\n',
        '1,2,2\n',
        '3,2,2\n',
        '2,1,2\n',
        '2,3,2\n',
        '2,2,1\n',
        '2,2,3\n',
        '2,2,4\n',
        '2,2,6\n',
        '1,2,5\n',
        '3,2,5\n',
        '2,1,5\n',
        '2,3,5\n',
    ]


def test_convert():
    lines = data()
    scans = convert(lines)
    assert len(scans) == 13
    assert scans[0] == (2, 2, 2)


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 64


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 58
