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
    """
    Repräsentation für einen Blizzard
    """

    boundaries = None

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

    def is_relevant(self, position):
        if self.direction == directions.UP or self.direction == directions.DOWN:
            return abs(self.col - position[1]) <= 1
        return abs(self.row - position[0]) <= 1


class Maze:
    """
    Repräsentation des Blizzard Basin
    """
    def __init__(self, lines):
        self.entry = (0, lines[0].index("."))
        self.exit = (len(lines) - 1, lines[-1].index("."))
        self.size = (1, 1, len(lines) - 2, len(lines[0]) - 2)
        self.loop_len = lcm(self.size[2]-self.size[0]+1, self.size[3]-self.size[1]+1)
        self.blizzards = []
        for row in range(self.size[0], self.size[2] + 1):
            for col in range(self.size[1], self.size[3] + 1):
                if lines[row][col] != ".":
                    self.blizzards.append(Blizzard(self.size, row, col, lines[row][col]))

    def possible_next_pos(self, player, minute):
        """
        Ermittlung der möglichen freien Felder für den Spieler in der nächsten Minute,
        wenn der Spieler
        :param player: Position des Spielers zur aktuellen Minute
        :param minute: aktuelle Minute
        :return: Menge an möglichen Positionen
        """
        row, col = player
        # Alle Nachbarfelder des Spielers
        positions = [(row + 1, col), (row, col), (row - 1, col),  (row, col - 1), (row, col + 1)]
        # Reduzierung aufs Spielfeld
        positions = set(filter(lambda p: self.valid_position(p), positions))
        # Reduzierung um Blizzard-Positionen in der Nähe
        for blizzard in self.blizzards:
            if blizzard.is_relevant(player):
                position = blizzard.position(minute+1)
                positions.discard(position)
        return positions

    def valid_position(self, position):
        """
        Erlaubt sind prinzipell alle Positionen im Rechteck
        zzgl. des Eingangs und des Ausgangs
        """
        if position == self.entry or position == self.exit:
            return True
        return self.size[0] <= position[0] <= self.size[2] and self.size[1] <= position[1] <= self.size[3]

    def distance_to_goal(self, position, goal):
        """
        Für A*-Algorithmus: Schätzwert, wie weit es minimal noch bis zum Ziel ist
        """
        return abs(goal[0] - position[0]) + abs(goal[1] - position[1])



def solve01(lines: List[str]) -> int:
    """
    Suche des kürzesten Weges vom Eingang zum Ausgang
    """
    maze = convert(lines)
    return find_way(maze, maze.entry, maze.exit, 0)


def find_way(maze, start, goal, start_minute):
    """
    Findet den kürzesten Pfad vom Start zum Ziel mit Hilfe des A*-Algorithmus
    """
    explored = set()
    already_explored = 0
    already_queued = 0
    queue = set([(start, start_minute)])
    while queue:
        situation = best_in_queue(maze, queue, goal)
        player, minute = situation
        queue.discard(situation)
        explored.add(situation)
        positions = maze.possible_next_pos(player, minute)
        if goal in positions:
            print(f"reduced by explored: {already_explored}")
            print(f"reduced by queue: {already_queued}")
            return minute + 1
        for position in positions:
            new_situation = (position, minute+1)
            if new_situation in queue:
                already_queued += 1
                continue
            if new_situation in explored:
                already_explored += 1
                continue
            queue.add((position, minute+1))


def best_in_queue(maze, queue, goal):
    """
    Ermitteln der Situation in der Queue, die lt. Heuristik die beste Aussicht hat, auf dem kürzesten Pfad
    zu liegen.
    """
    return min(queue, key=lambda tup: tup[1] + maze.distance_to_goal(tup[0], goal))


def solve02(lines: List[str]) -> int:
    """
    Suche des kürzesten Weges vom Eingang zum Ausgang,
    anschließend vom Ausgang zum Eingang
    und wieder zurück zum Ausgang
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
    Umwandeln des Inputs in ein Spielfeld
    """
    return Maze(list(map(lambda l: l.strip(), lines)))


def lcm(a, b):
    """
    KGV zweier Zahlen
    """
    def gcd(a, b):
        if b == 0:
            return a
        return gcd(b, a % b)

    return a * b // gcd(a, b)


if __name__ == '__main__':
    lines = read_puzzle("data/day24.txt")
    side2 = pfc()
    print(solve01(lines), pfc() - side2)
    side2 = pfc()
    print(solve02(lines), pfc() - side2)
