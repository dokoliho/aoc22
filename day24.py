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


class Blizzard:
    def __init__(self, boundaries, row, col, char):
        self.boundaries = boundaries
        self.row = row
        self.col = col
        match char:
            case ">":
                self.direction = directions.RIGHT
            case "<":
                self.direction = directions.LEFT
            case "^":
                self.direction = directions.UP
            case "v":
                self.direction = directions.DOWN
            case other:
                raise Exception(f"Illegal char {char}")

    def position(self, minute):
        match self.direction:
            case directions.RIGHT:
                return self.row, ((self.col + minute - 1) % self.boundaries[3]) + 1
            case directions.LEFT:
                return self.row, ((self.col - minute - 1) % self.boundaries[3]) + 1
            case directions.UP:
                return ((self.row - minute - 1) % self.boundaries[2]) + 1, self.col
            case directions.DOWN:
                return ((self.row + minute - 1) % self.boundaries[2]) + 1, self.col


class Maze:
    def __init__(self, lines):
        self.entry = (0, lines[0].index("."))
        self.exit = (len(lines)-1, lines[-1].index("."))
        self.size = (1, 1, len(lines)-2, len(lines[0])-2)
        self.blizzards = []
        for row in range(self.size[0], self.size[2]+1):
            for col in range(self.size[1], self.size[3] + 1):
                if lines[row][col] != ".":
                    self.blizzards.append(Blizzard(self.size, row, col, lines[row][col]))

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
    return Maze(list(map(lambda l: l.strip(), lines)))


if __name__ == '__main__':
    lines = read_puzzle("data/day24.txt")
    side2 = pfc()
    print(solve01(lines), pfc() - side2)
    side2 = pfc()
    print(solve02(lines), pfc() - side2)
