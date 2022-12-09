from typing import List
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    """
    return 0


def solve02(lines: List[str]) -> int:
    """
    """
    return 0

def convert(lines: List[str]):
    tuples =  map(lambda l: tuple(l.strip().split()), lines)
    return list(map(lambda tup: (tup[0], int(tup[1])), tuples))


if __name__ == '__main__':
    lines = read_puzzle("data/day9.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

