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


def new_tail_after_close_gap(head, tail):
    if are_close(head, tail):
        return tail
    dx = 0
    dy = 0
    if abs(head[0]-tail[0]) > 0:
        dx = 1 if head[0] > tail[0] else -1
    if abs(head[1]-tail[1]) > 0:
        dy = 1 if head[1] > tail[1] else -1
    return tail[0]+dx, tail[1]+dy


def are_close(head, tail):
    return abs(head[0]-tail[0]) <= 1 and abs(head[1]-tail[1]) <= 1


def move_one_step(start, direction):
    match direction:
        case 'R':
            return start[0] + 1, start[1]
        case 'L':
            return start[0] - 1, start[1]
        case 'U':
            return start[0], start[1] - 1
        case 'D':
            return start[0] , start[1] + 1
    return start


if __name__ == '__main__':
    lines = read_puzzle("data/day9.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

