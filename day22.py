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

DIR_UP = Direction(3)
DIR_DOWN = Direction(1)
DIR_RIGHT = Direction(0)
DIR_LEFT = Direction(2)


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
            return (row, col), direction, True
        if tile == "#":
            return (position[0], position[1]), direction, False

    def move_path(self, position, direction, path):
        for token in path:
            if isinstance(token, int):
                for _ in range(token):
                    position, direction, cont = self.move_one_step(position, direction)
                    if cont is False:
                        break
            else:
                if token == "R":
                    direction.turn_right()
                if token == "L":
                    direction.turn_left()
        return position, direction


class CubeMaze(Maze):

    def get_side_len(self):
        if len(self.lines) == len(self.lines[0]):
            return len(self.lines) // 3
        else:
            larger = max(len(self.lines), len(self.lines[0]))
            return larger // 4

    def get_side_lines(self, side_row, side_col):
        side_len = self.get_side_len()
        if side_row * side_len > len(self.lines) or side_col * side_len > len(self.lines[0]):
            return self.empty_side()
        selected_lines = self.lines[side_row*side_len:(side_row+1)*side_len]
        return list(map(lambda l: l[side_col*side_len:(side_col+1*side_len)], selected_lines))

    def empty_side(self):
        side_len = self.get_side_len()
        empty_line = " " * side_len
        return [empty_line for _ in range(side_len)]

    def get_local_position_on_side(self, position):
        row, col = position
        side_len = self.get_side_len()
        return (row % side_len, col % side_len)

    def get_side(self, position):
        row, col = position
        side_len = self.get_side_len()
        return row // side_len, col // side_len

    def get_global_position(self, side_row, side_col, local_position):
        row, col = local_position
        side_len = self.get_side_len()
        side_rows = len(self.lines) // side_len
        side_cols = len(self.lines[0]) // side_len
        side_row = (side_row + side_rows) % side_rows
        side_col = (side_col + side_cols) % side_cols
        return side_row * side_len + row, side_col * side_len + col

    def move_one_step(self, position, direction: Direction):
        side_pos = self.get_side(position)
        row, col = position
        new_row = row + direction.delta_row()
        new_col = col + direction.delta_col()
        new_direction = direction
        if side_pos != self.get_side((new_row, new_col)):
            if direction == DIR_UP:
                (new_row, new_col), new_direction = self.row_underrun((row, col))
            if direction == DIR_DOWN:
                (new_row, new_col), new_direction = self.row_overrun((row, col))
            if direction == DIR_LEFT:
                (new_row, new_col), new_direction = self.col_underrun((row, col))
            if direction == DIR_RIGHT:
                (new_row, new_col), new_direction = self.col_overrun((row, col))
        tile = self.get_tile(new_row, new_col)
        if tile == ".":
            return (new_row, new_col), new_direction, True
        if tile == "#":
            return (row, col), direction, False

    def row_underrun(self, position):
        side_len = self.get_side_len()
        side_position = self.get_local_position_on_side(position)
        row, col = side_position
        side_row, side_col = self.get_side(position)
        # upper
        position = self.get_global_position(side_row - 1, side_col, (side_len-1, col))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_UP
        # upper left
        position = self.get_global_position(side_row - 1, side_col - 1, (side_len - col - 1, side_len - 1))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_LEFT
        # upper right
        position = self.get_global_position(side_row - 1, side_col + 1, (col, 0))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_RIGHT
        # upper double left
        position = self.get_global_position(side_row - 1, side_col - 2, (0, side_len - col - 1))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_DOWN
        # upper double right
        position = self.get_global_position(side_row - 1, side_col + 2, (0, side_len - col - 1))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_DOWN
        raise Exception("No Continuation found")

    def row_overrun(self, position):
        side_len = self.get_side_len()
        side_position = self.get_local_position_on_side(position)
        row, col = side_position
        side_row, side_col = self.get_side(position)
        # lower
        position = self.get_global_position(side_row + 1, side_col, (0, col))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_DOWN
        # lower left
        position = self.get_global_position(side_row + 1, side_col - 1, (col, side_len - 1))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_LEFT
        # lower right
        position = self.get_global_position(side_row + 1, side_col + 1, (side_len - col - 1, 0))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_RIGHT
        # lower double left
        position = self.get_global_position(side_row + 1, side_col - 2, (side_len - 1, side_len - col - 1))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_UP
        # lower double right
        position = self.get_global_position(side_row + 1, side_col + 2, (side_len - 1, side_len - col - 1))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_UP
        raise Exception("No Continuation found")

    def col_underrun(self, position):
        side_len = self.get_side_len()
        local_position = self.get_local_position_on_side(position)
        row, col = local_position
        side_row, side_col = self.get_side(position)
        # left
        position = self.get_global_position(side_row, side_col - 1, (row, side_len - 1))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_LEFT
        # left upper
        position = self.get_global_position(side_row - 1, side_col - 1, (side_len - 1, side_len - col - 1))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_UP
        # left lower
        if side_col == 0:
            position = self.get_global_position(side_row + 1, side_col - 1, (side_len-1, side_len - row - 1))
            if self.get_tile(position[0], position[1]) != " ":
                return position, DIR_UP
        else:
            position = self.get_global_position(side_row + 1, side_col - 1, (0, row))
            if self.get_tile(position[0], position[1]) != " ":
                return position, DIR_DOWN
        # left double upper
        position = self.get_global_position(side_row - 2, side_col - 1, (side_len - row - 1, 0))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_RIGHT
        # left double lower
        position = self.get_global_position(side_row + 2, side_col - 1, (side_len - row - 1, 0))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_RIGHT
        raise Exception("No Continuation found")

    def col_overrun(self, position):
        side_len = self.get_side_len()
        side_position = self.get_local_position_on_side(position)
        row, col = side_position
        side_row, side_col = self.get_side(position)
        # right
        position = self.get_global_position(side_row, side_col + 1, (row, 0))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_RIGHT
        # right upper
        position = self.get_global_position(side_row - 1, side_col + 1, (side_len - 1, row))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_UP
        # right lower
        position = self.get_global_position(side_row + 1, side_col + 1, (0, side_len - row - 1))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_DOWN
        # right double upper
        position = self.get_global_position(side_row - 2, side_col + 1, (side_len-row-1, side_len - 1))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_LEFT
        # right double lower
        position = self.get_global_position(side_row + 2, side_col + 1, (side_len-row-1, side_len - 1))
        if self.get_tile(position[0], position[1]) != " ":
            return position, DIR_LEFT
        raise Exception("No Continuation found")


def solve01(lines: List[str]) -> int:
    """
    """
    maze, path = convert(lines)
    position = maze.start_position()
    direction = DIR_RIGHT
    (row, col), end_direction = maze.move_path(position, direction, path)
    return 1000 * (row + 1) + 4 * (col + 1) + end_direction.facing


def solve02(lines: List[str]) -> int:
    """
    """
    maze, path = convertCube(lines)
    position = maze.start_position()
    direction = DIR_RIGHT
    (row, col), end_direction = maze.move_path(position, direction, path)
    return 1000 * (row + 1) + 4 * (col + 1) + end_direction.facing


def convert(lines):
    """
    """
    lines = list(map(lambda l: l[:-1], lines))
    return Maze(lines[:-2]), convert_command(lines[-1])


def convertCube(lines):
    """
    """
    lines = list(map(lambda l: l[:-1], lines))
    return CubeMaze(lines[:-2]), convert_command(lines[-1])



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
