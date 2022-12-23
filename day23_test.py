from typing import List
from day23 import solve01, solve02, convert, Plan

def data() -> List[str]:
    return [
        '....#..\n',
        '..###.#\n',
        '#...#.#\n',
        '.#...##\n',
        '#.###..\n',
        '##.#.##\n',
        '.#..#..\n',
    ]


def small_data() -> List[str]:
    return [
        '.....\n',
        '..##.\n',
        '..#..\n',
        '.....\n',
        '..##.\n',
        '.....\n',
    ]


def test_convert():
    lines = data()
    plan = convert(lines)
    assert plan.elves_count == 22


def test_proposal():
    lines = small_data()
    plan = convert(lines)
    proposals = plan.generate_proposals()
    assert len(proposals) == 4


def test_move():
    lines = small_data()
    plan = convert(lines)
    plan.generate_proposals()
    count = plan.move_elves()
    assert count == 3


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 110


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 20


