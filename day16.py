from typing import List
import re
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def convert_to_valves(lines):
    valves = {}
    for line in lines:
        name, rate, destinations = convert_line_to_valve(line.strip())
        valves[name] = (rate, destinations)
    return valves


def convert_line_to_valve(line):
    m = re.search(r'Valve (\S+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)$', line)
    name, rate, destinations = m.groups()
    destinations = list(map(lambda d: d.strip(), destinations.split(",")))
    return name, int(rate), destinations


def solve01(lines: List[str]) -> int:
    """
    """
    return 0


def solve02(lines: List[str]) -> int:
    """
    """
    return 0


if __name__ == '__main__':
    lines = read_puzzle("data/day14.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

