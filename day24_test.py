from typing import List
from day24 import solve01, solve02, convert

def data() -> List[str]:
    return [
        '#.######\n',
        '#>>.<^<#\n',
        '#.<..<<#\n',
        '#>v.><>#\n',
        '#<^v^^>#\n',
        '######.#\n',
    ]


def test_convert():
    lines = data()
    maze = convert(lines)
    assert maze.entry == (0, 1)
    assert maze.exit == (5, 6)
    assert maze.size == (1, 1, 4, 6)
    assert len(maze.blizzards) == 19

def test_blizzard_movement():
    lines = data()
    maze = convert(lines)
    blizzard = maze.blizzards[0]
    assert blizzard.position(0) == (1, 1)
    assert blizzard.position(1) == (1, 2)
    assert blizzard.position(2) == (1, 3)
    assert blizzard.position(6) == (1, 1)
    blizzard = maze.blizzards[3]
    assert blizzard.position(0) == (1, 5)
    assert blizzard.position(1) == (4, 5)
    assert blizzard.position(2) == (3, 5)
    blizzard = maze.blizzards[5]
    assert blizzard.position(0) == (2, 2)
    assert blizzard.position(1) == (2, 1)
    assert blizzard.position(2) == (2, 6)
    blizzard = maze.blizzards[9]
    assert blizzard.position(0) == (3, 2)
    assert blizzard.position(1) == (4, 2)
    assert blizzard.position(2) == (1, 2)




def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 0


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 0


