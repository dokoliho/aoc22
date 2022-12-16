from typing import List
from day16 import solve01, solve02
from day16 import convert_line_to_valve, convert_to_valves




def data() -> List[str]:
    return [
        'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB\n',
        'Valve BB has flow rate=13; tunnels lead to valves CC, AA\n',
        'Valve CC has flow rate=2; tunnels lead to valves DD, BB\n',
        'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE\n',
        'Valve EE has flow rate=3; tunnels lead to valves FF, DD\n',
        'Valve FF has flow rate=0; tunnels lead to valves EE, GG\n',
        'Valve GG has flow rate=0; tunnels lead to valves FF, HH\n',
        'Valve HH has flow rate=22; tunnel leads to valve GG\n',
        'Valve II has flow rate=0; tunnels lead to valves AA, JJ\n',
        'Valve JJ has flow rate=21; tunnel leads to valve II\n',
    ]


def test_convert_line_to_valve():
    lines = data()
    name, rate, destinations = convert_line_to_valve(lines[0].strip())
    assert name == 'AA'
    assert rate == 0
    assert destinations == ['DD', 'II', 'BB']


def test_convert():
    lines = data()
    valves = convert_to_valves(lines)
    assert len(valves) == 10


def test_solve1():
    lines: List[str] = data()
    result: int = solve01(lines)
    assert result == 1651


def test_solve2():
    lines: List[str] = data()
    result: int = solve02(lines)
    assert result == 1707
