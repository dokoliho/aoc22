from typing import List
import types
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


directions = types.SimpleNamespace()
directions.RIGHT = 0
directions.DOWN = 1
directions.LEFT = 2
directions.UP = 3


class Transition:
    def __init__(self, row_func, col_func):
        self.row_func = row_func
        self.col_func = col_func

    def calc_row(self, row, col, mlen):
        return self.row_func(row, col, mlen)

    def calc_col(self, row, col, mlen):
        return self.col_func(row, col, mlen)

    @staticmethod
    def transition_sequence(t1,  t2):
        return Transition(
            lambda row, col, mlen: t2.row_func(t1.row_func(row, col, mlen), t1.col_func(row, col, mlen), mlen),
            lambda row, col, mlen: t2.col_func(t1.row_func(row, col, mlen), t1.col_func(row, col, mlen), mlen)
        )

    def __repr__(self):
        return "Transition"

class Direction:

    def __init__(self, facing):
        self.facing = facing % 4

    def turn_right(self):
        self.facing = (self.facing + 1) % 4

    def turn_left(self):
        self.turn_right()
        self.turn_right()
        self.turn_right()

    def delta_row(self):
        match self.facing:
            case directions.RIGHT:
                return 0
            case directions.DOWN:
                return 1
            case directions.LEFT:
                return 0
            case directions.UP:
                return -1

    def delta_col(self):
        match self.facing:
            case directions.RIGHT:
                return 1
            case directions.DOWN:
                return 0
            case directions.LEFT:
                return -1
            case directions.UP:
                return 0


DIR_UP = Direction(directions.UP)
DIR_DOWN = Direction(directions.DOWN)
DIR_RIGHT = Direction(directions.RIGHT)
DIR_LEFT = Direction(directions.LEFT)


class Maze:

    def __init__(self, lines):
        max_len = max(map(len, lines))
        self.lines = list(map(lambda l: l.ljust(max_len), lines))

    def start_position(self):
        for row, line in enumerate(self.lines):
            col = line.find(".")
            if col >= 0:
                return row, col
        raise Exception("No starting position")

    def get_tile(self, position):
        row, col = position
        return self.lines[row][col]

    def move_one_step(self, position, direction: Direction):
        row, col = position
        tile = " "
        while tile == " ":
            row = (row + direction.delta_row()) % len(self.lines)
            col = (col + direction.delta_col()) % len(self.lines[row])
            tile = self.get_tile((row, col))
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


class Side:
    def __init__(self, top, left):
        self.connected = {}
        self.top = top
        self.left = left

    def __repr__(self):
        return f"({self.top}, {self.left})"


class CubeMaze(Maze):

    def __init__(self, lines):
        super().__init__(lines)
        slen = self.get_side_len()
        self.sides = []
        for row in range(0, len(self.lines), slen):
            for col in range(0, len(self.lines[0]), slen):
                if self.get_tile((row, col)) != " ":
                    self.sides.append(Side(row, col))
        assert len(self.sides) == 6
        self.create_initial_connections()
        self.complete_connections()

    def create_initial_connections(self):
        slen = self.get_side_len()
        for index, side1 in enumerate(self.sides):
            for side2 in self.sides[index + 1:]:
                if side1.top == side2.top:
                    if side1.left == side2.left - slen:
                        side1.connected[directions.RIGHT] = (side2, 0)
                        side2.connected[directions.LEFT] = (side1, 0)
                    if side1.left == side2.left + slen:
                        side1.connected[directions.LEFT] = (side2, 0)
                        side2.connected[directions.RIGHT] = (side1, 0)
                if side1.left == side2.left:
                    if side1.top == side2.top - slen:
                        side1.connected[directions.DOWN] = (side2, 0)
                        side2.connected[directions.UP] = (side1, 0)
                    if side1.top == side2.top + slen:
                        side1.connected[directions.UP] = (side2, 0)
                        side2.connected[directions.DOWN] = (side1, 0)

    def complete_connections(self):
        added = False
        for side in self.sides:
            for direction in range(4):
                if side.connected.get(direction) is None:
                    added = added or self.check_and_add(side, direction)
        if added:
            self.complete_connections()

    def check_and_add(self, side, direction):
        for deroute in [-1, 1]:
            deroute_direction = (direction + deroute) % 4
            if side.connected.get(deroute_direction):
                middle, middle_turn = side.connected.get(deroute_direction)
                check_direction = (direction + middle_turn + 4 ) % 4
                if middle.connected.get(check_direction):
                    target, target_turn = middle.connected.get(check_direction)
                    side.connected[direction] = (target, (middle_turn + target_turn + deroute + 4) % 4)
                    return True
        return False


    def get_side_by_position(self, sides, top, left):
        for side in sides:
            if side.left == left and side.top == top:
                return side
        return None


    def get_side_len(self):
        if len(self.lines) == len(self.lines[0]):
            return len(self.lines) // 3
        else:
            larger = max(len(self.lines), len(self.lines[0]))
            return larger // 4

    def get_local_position_on_side(self, position):
        row, col = position
        side_len = self.get_side_len()
        return (row + side_len) % side_len, (col + side_len) % side_len

    def move_one_step(self, position, direction: Direction):
        current_side_index = self.get_side_index(position)
        new_position = self.new_position_after_step(position, direction)
        new_side_index = self.get_side_index(new_position)
        new_direction = direction
        if current_side_index != new_side_index:
            local_row, local_col = self.get_local_position_on_side(new_position)
            mlen = self.get_side_len() - 1
            new_side, turn = self.sides[current_side_index].connected[direction.facing]
            new_direction = Direction((direction.facing + turn + 4) % 4)
            transitions = [
                [(local_row, 0), (0, mlen - local_row), (mlen - local_row, mlen), (mlen, local_row)],     # Right
                [(0, local_col), (local_col, mlen), (mlen, mlen - local_col), (mlen - local_col, 0)],     # Down
                [(local_row, mlen), (mlen, mlen-local_row), (mlen-local_row, 0), (0, local_row)],     # Left
                [(mlen, local_col), (local_col, 0), (0, mlen-local_col), (mlen-local_col, mlen)],   # Up
            ]
            new_row, new_col = transitions[direction.facing][turn]
            new_position = (new_side.top + new_row, new_side.left + new_col)
        tile = self.get_tile(new_position)
        if tile == ".":
            return new_position, new_direction, True
        if tile == "#":
            return position, direction, False

    @staticmethod
    def new_position_after_step(position, direction: Direction):
        curr_row, curr_col = position
        new_row = curr_row + direction.delta_row()
        new_col = curr_col + direction.delta_col()
        return new_row, new_col

    def get_side_index(self, position):
        side_len = self.get_side_len()
        for index, side in enumerate(self.sides):
            if side.left <= position[1] < side.left + side_len and side.top <= position[0] < side.top + side_len:
                return index
        return None


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
    maze, path = convert_cube(lines)
    position = maze.start_position()
    direction = DIR_RIGHT
    (row, col), end_direction = maze.move_path(position, direction, path)
    return 1000 * (row + 1) + 4 * (col + 1) + end_direction.facing


def convert(lines):
    """
    """
    lines = list(map(lambda l: l[:-1], lines))
    return Maze(lines[:-2]), convert_command(lines[-1])


def convert_cube(lines):
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
    side2 = pfc()
    print(solve01(lines), pfc() - side2)
    side2 = pfc()
    print(solve02(lines), pfc() - side2)
