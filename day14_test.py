import functools
from typing import List
from day14 import solve01, solve02, convert_to_rock_set, pour_one_sand_unit


def data() -> List[str]:
    return [
        '498,4 -> 498,6 -> 496,6\n',
        '503,4 -> 502,4 -> 502,9 -> 494,9\n',
     ]


def test_convert():
    rocks = convert_to_rock_set(data())
    assert len(rocks) == 20
    assert (494, 9) in rocks
    assert (495, 9) in rocks
    assert (496, 6) in rocks
    assert (498, 5) in rocks


def test_pour_one_unit():
    rocks = convert_to_rock_set(data())
    sand = set()
    fall = pour_one_sand_unit((500, 0), rocks, sand)
    assert (500,8) in sand
    assert len(sand) == 1
    assert not fall
    fall = pour_one_sand_unit((500, 0), rocks, sand)
    assert (499,8) in sand
    assert len(sand) == 2
    assert not fall


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 24


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 93
