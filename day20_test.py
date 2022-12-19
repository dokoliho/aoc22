from typing import List
from day20 import solve01, solve02, convert

def data() -> List[str]:
    return [
        'Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.\n',
        'Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.\n',
    ]


def test_convert():
    lines = data()




def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 0


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 0
