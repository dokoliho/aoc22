from typing import List
import types
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


def convert(lines):
    """
    """
    return lines


if __name__ == '__main__':
    lines = read_puzzle("data/day25.txt")
    side2 = pfc()
    print(solve01(lines), pfc() - side2)
    side2 = pfc()
    print(solve02(lines), pfc() - side2)
