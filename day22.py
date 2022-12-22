from typing import List
import re
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


class Maze():

    def __init__(self, lines):
        self.lines = lines

    def start_position(self):
        for row, line in enumerate(self.lines):
            col = line.find(".")
            if col >=0:
                return row, col
        raise Exception("No starting position")


def solve01(lines: List[str]) -> int:
    """
    """
    return 0


def solve02(lines: List[str]) -> int:
    """
    """
    return 0


def convert(lines):
    """
    """
    lines = list(map(lambda l: l[:-1], lines))
    return Maze(lines[:-2]), lines[-1]




if __name__ == '__main__':
    lines = read_puzzle("data/day22.txt")
    start = pfc()
    print(solve01(lines), pfc() - start)
    start = pfc()
    print(solve02(lines), pfc() - start)
