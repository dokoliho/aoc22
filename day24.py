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
        self.exit = (len(lines) - 1, lines[-1].index("."))
        self.size = (1, 1, len(lines) - 2, len(lines[0]) - 2)
        self.loop_len = (self.size[2]-self.size[0]+1)*(self.size[3]-self.size[1]+1)   # besser: kgv
        self.blizzards = []
        for row in range(self.size[0], self.size[2] + 1):
            for col in range(self.size[1], self.size[3] + 1):
                if lines[row][col] != ".":
                    self.blizzards.append(Blizzard(self.size, row, col, lines[row][col]))

    def possible_next_pos(self, player, minute):
        row, col = player
        positions = [(row + 1, col), (row, col), (row - 1, col),  (row, col - 1), (row, col + 1)]
        positions = set(filter(lambda p: self.valid_position(p), positions))
        for blizzard in self.blizzards:
            position = blizzard.position(minute+1)
            positions.discard(position)
        return positions

    def valid_position(self, position):
        if position == self.entry or position == self.exit:
            return True
        return self.size[0] <= position[0] <= self.size[2] and self.size[1] <= position[1] <= self.size[3]

    def distance_to_goal(self, position, goal):
        return abs(goal[0] - position[0]) + abs(goal[1] - position[1])

    def canonical_situation(self, situation):
        position, minute = situation
        return position, minute % self.loop_len


def solve01(lines: List[str]) -> int:
    """
    """
    maze = convert(lines)
    return find_way(maze, maze.entry, maze.exit, 0)


def find_way(maze, start, goal, start_minute):
    explored = []
    queue = [(start, start_minute)]
    while queue:
        situation = best_in_queue(maze, queue, goal)
        player, minute = situation
        queue.remove(situation)
        explored.append(situation)
        positions = maze.possible_next_pos(player, minute)
        if goal in positions:
            return minute + 1
        for position in positions:
            new_situation = (position, minute+1)
            if new_situation not in explored and new_situation not in queue:
                queue.append((position, minute+1))


def best_in_queue(maze, queue, goal):
    return min(queue, key=lambda tup: tup[1] + maze.distance_to_goal(tup[0], goal))


def solve02(lines: List[str]) -> int:
    """
    """
    maze = convert(lines)
    duration = find_way(maze, maze.entry, maze.exit, 0)
    print(f"From entry to exit in {duration} minutes")
    duration = find_way(maze, maze.exit, maze.entry, duration)
    print(f"Back at entry after {duration} minutes")
    duration = find_way(maze, maze.entry, maze.exit, duration)
    print(f"Finally back at exit after {duration} minutes")
    return duration


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
