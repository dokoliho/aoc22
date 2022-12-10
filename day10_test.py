from typing import List
from day10 import solve01, solve02, convert, register_values, get_line


def data() -> List[str]:
    return [
        'addx 15\n',
        'addx -11\n',
        'addx 6\n',
        'addx -3\n',
        'addx 5\n',
        'addx -1\n',
        'addx -8\n',
        'addx 13\n',
        'addx 4\n',
        'noop\n',
        'addx -1\n',
        'addx 5\n',
        'addx -1\n',
        'addx 5\n',
        'addx -1\n',
        'addx 5\n',
        'addx -1\n',
        'addx 5\n',
        'addx -1\n',
        'addx -35\n',
        'addx 1\n',
        'addx 24\n',
        'addx -19\n',
        'addx 1\n',
        'addx 16\n',
        'addx -11\n',
        'noop\n',
        'noop\n',
        'addx 21\n',
        'addx -15\n',
        'noop\n',
        'noop\n',
        'addx -3\n',
        'addx 9\n',
        'addx 1\n',
        'addx -3\n',
        'addx 8\n',
        'addx 1\n',
        'addx 5\n',
        'noop\n',
        'noop\n',
        'noop\n',
        'noop\n',
        'noop\n',
        'addx -36\n',
        'noop\n',
        'addx 1\n',
        'addx 7\n',
        'noop\n',
        'noop\n',
        'noop\n',
        'addx 2\n',
        'addx 6\n',
        'noop\n',
        'noop\n',
        'noop\n',
        'noop\n',
        'noop\n',
        'addx 1\n',
        'noop\n',
        'noop\n',
        'addx 7\n',
        'addx 1\n',
        'noop\n',
        'addx -13\n',
        'addx 13\n',
        'addx 7\n',
        'noop\n',
        'addx 1\n',
        'addx -33\n',
        'noop\n',
        'noop\n',
        'noop\n',
        'addx 2\n',
        'noop\n',
        'noop\n',
        'noop\n',
        'addx 8\n',
        'noop\n',
        'addx -1\n',
        'addx 2\n',
        'addx 1\n',
        'noop\n',
        'addx 17\n',
        'addx -9\n',
        'addx 1\n',
        'addx 1\n',
        'addx -3\n',
        'addx 11\n',
        'noop\n',
        'noop\n',
        'addx 1\n',
        'noop\n',
        'addx 1\n',
        'noop\n',
        'noop\n',
        'addx -13\n',
        'addx -19\n',
        'addx 1\n',
        'addx 3\n',
        'addx 26\n',
        'addx -30\n',
        'addx 12\n',
        'addx -1\n',
        'addx 3\n',
        'addx 1\n',
        'noop\n',
        'noop\n',
        'noop\n',
        'addx -9\n',
        'addx 18\n',
        'addx 1\n',
        'addx 2\n',
        'noop\n',
        'noop\n',
        'addx 9\n',
        'noop\n',
        'noop\n',
        'noop\n',
        'addx -1\n',
        'addx 2\n',
        'addx -37\n',
        'addx 1\n',
        'addx 3\n',
        'noop\n',
        'addx 15\n',
        'addx -21\n',
        'addx 22\n',
        'addx -6\n',
        'addx 1\n',
        'noop\n',
        'addx 2\n',
        'addx 1\n',
        'noop\n',
        'addx -10\n',
        'noop\n',
        'noop\n',
        'addx 20\n',
        'addx 1\n',
        'addx 2\n',
        'addx 2\n',
        'addx -6\n',
        'addx -11\n',
        'noop\n',
        'noop\n',
        'noop\n',
    ]

def test_convert():
    lines = data()
    result = convert(lines)
    assert result[0] == ('addx', 15)
    assert result[-1] == ('noop', None)


def test_register_values():
    lines = data()
    commands = convert(lines)
    values = list(register_values(commands))
    assert values[19] == 21
    assert values[59] == 19
    assert values[99] == 18
    assert values[139] == 21
    assert values[179] == 16
    assert values[219] == 18


def test_get_line():
    expected_lines = [
        "##..##..##..##..##..##..##..##..##..##..",
        "###...###...###...###...###...###...###.",
        "####....####....####....####....####....",
        "#####.....#####.....#####.....#####.....",
        "######......######......######......####",
        "#######.......#######.......#######.....",
    ]
    lines = data()
    commands = convert(lines)
    values = list(register_values(commands))
    for line_index in range(6):
        assert get_line(line_index, values) == expected_lines[line_index]


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 13140


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 0
