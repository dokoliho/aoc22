from typing import List
import re
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


class Direction():

    def __init__(self, facing):
        self.facing = facing

    def turn_right(self):
        self.facing = (self.facing + 1) % 4

    def turn_left(self):
        self.turn_right()
        self.turn_right()
        self.turn_right()

    def delta_row(self):
        match self.facing:
            case 0: return 0
            case 1: return 1
            case 2: return 0
            case 3: return -1

    def delta_col(self):
        match self.facing:
            case 0: return 1
            case 1: return 0
            case 2: return -1
            case 3: return 0


class Maze():

    def __init__(self, lines):
        max_len = max(map(len, lines))
        self.lines = list(map(lambda l: l.ljust(max_len), lines))

    def start_position(self):
        for row, line in enumerate(self.lines):
            col = line.find(".")
            if col >=0:
                return row, col
        raise Exception("No starting position")

    def get_tile(self, row, col):
        return self.lines[row][col]

    def move_one_step(self, position, direction: Direction):
        row, col = position
        tile = " "
        while tile == " ":
            row = (row + direction.delta_row()) % len(self.lines)
            col = (col + direction.delta_col()) % len(self.lines[row])
            tile = self.get_tile(row, col)
        if tile == ".":
            return (row, col), True
        if tile == "#":
            return (position[0], position[1]), False

    def move_path(self, position, direction, path):
        for token in path:
            if isinstance(token, int):
                for _ in range(token):
                    position, cont = self.move_one_step(position, direction)
                    if cont is False:
                        break
            else:
                if token == "R":
                    direction.turn_right()
                if token == "L":
                    direction.turn_left()
        return position, direction


def solve01(lines: List[str]) -> int:
    """
    """
    maze, path = convert(lines)
    position = maze.start_position()
    direction = Direction(0)
    (row, col), end_direction = maze.move_path(position, direction, path)
    return 1000 * (row + 1) + 4 * (col + 1) + end_direction.facing


def solve02(lines: List[str]) -> int:
    """
    """
    return 0


def convert(lines):
    """
    """
    lines = list(map(lambda l: l[:-1], lines))
    return Maze(lines[:-2]), convert_command(lines[-1])


def convert_command(command):
    result = []
    i = 0
    while i < len(command):
        if command[i].isdigit():
            j = i
            while j < len(command) and command[j].isdigit():
                j += 1
            result.append(int(command[i:j]))
            i = j
        else:
            result.append(command[i])
            i += 1
    return result


if __name__ == '__main__':
    lines = read_puzzle("data/day22.txt")
    start = pfc()
    print(solve01(lines), pfc() - start)
    start = pfc()
    print(solve02(lines), pfc() - start)
