from typing import List
from day25 import solve01, solve02, convert, snafu_to_dec, rjust_snafu, add_snafus

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


def test_snafu_to_dec():
    lines = data()
    snafus = convert(lines)
    decs = list(map(lambda s: snafu_to_dec(s), snafus))
    assert decs == [1747, 906, 198, 11, 201, 31, 1257, 32, 353, 107, 7, 3, 37]


def test_rjust():
    snafu = "1-12"
    snafu = rjust_snafu(snafu, 10)
    assert snafu == "0000001-12"
    snafu = "1-12"
    snafu = rjust_snafu(snafu, 3)
    assert snafu == "1-12"


def test_add():
    lines = data()
    snafus = convert(lines)
    decs = list(map(lambda s: snafu_to_dec(s), snafus))
    result = add_snafus(snafus[0], snafus[1])
    assert snafu_to_dec(result) == decs[0] + decs[1]


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == "2=-1=0"


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 0


