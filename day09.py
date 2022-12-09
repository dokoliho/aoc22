from typing import List
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    """
    head = (0,0)
    tail = (0,0)
    movements = convert(lines)
    tail_positions = []
    for movement in movements:
        new_positions, head, tail = tail_positions_after_movement(head, tail, movement[0], movement[1])
        tail_positions = tail_positions + new_positions
    return len(set(tail_positions))


def solve02(lines: List[str]) -> int:
    """
    """
    snake = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
    movements = convert(lines)
    tail_positions = []
    for movement in movements:
        new_positions, snake = tail_positions_after_snake_movement(snake, movement[0], movement[1])
        tail_positions = tail_positions + new_positions
    return len(set(tail_positions))


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


def tail_positions_after_movement(head, tail, direction, count):
    result = [tail]
    for _ in range(count):
        head = move_one_step(head, direction)
        tail = new_tail_after_close_gap(head, tail)
        result.append(tail)
    return result, head, tail


def tail_positions_after_snake_movement(snake, direction, count):
    result = [snake[-1]]
    for _ in range(count):
        head = snake[0]
        snake[0] = move_one_step(head, direction)
        for i in range(len(snake)-1):
            snake[i+1] = new_tail_after_close_gap(snake[i], snake[i+1])
        result.append(snake[-1])
    return result, snake



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

