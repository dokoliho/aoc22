from typing import List
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    Ermitteln der Anzahl der Endepositionen
    Das Seil besteht nur aus Head und Tail
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
    Ermitteln der Anzahl der Endepositionen
    Das Seil besteht nur aus 10 Knoten, die gem. Regel aufeinander folgen
    """
    rope = [(0, 0) for _ in range(10)]
    movements = convert(lines)
    tail_positions = []
    for movement in movements:
        new_positions, rope = tail_positions_after_rope_movement(rope, movement[0], movement[1])
        tail_positions = tail_positions + new_positions
    return len(set(tail_positions))


def convert(lines: List[str]):
    """
    ['R 4\n', 'U 4\n', 'L 3\n', 'D 1\n', 'R 4\n', 'D 1\n', 'L 5\n', 'R 2\n'] ->
    [('R', 4), ('U', 4), ('L', 3), ('D', 1), ('R', 4), ('D', 1), ('L', 5), ('R', 2)]
    """
    tuples = map(lambda l: tuple(l.strip().split()), lines)
    return list(map(lambda tup: (tup[0], int(tup[1])), tuples))


def new_tail_after_close_gap(head, tail):
    """
    Implementierung der Nachfolgelogik
    Bewegung nur, wenn nicht zusammenstehend
    Bewegung aber in jede abweichende Dimension (d.h. auch diagonal)
    """
    if not(are_close(head, tail)):
        if abs(head[0]-tail[0]) > 0:
            tail = tail[0] + (1 if head[0] > tail[0] else -1), tail[1]
        if abs(head[1]-tail[1]) > 0:
            tail = tail[0], tail[1] + (1 if head[1] > tail[1] else -1)
    return tail


def are_close(head, tail):
    """
    Test auf zusammenstehend
    """
    return abs(head[0]-tail[0]) <= 1 and abs(head[1]-tail[1]) <= 1


def tail_positions_after_movement(head, tail, direction, count):
    """
    Durchführung einer Bewegungsfolge eine Seils mit Head und Tail
    Rückgabe der besuchten Positionen des Endes
    """
    rope = [head, tail]
    positions, rope =  tail_positions_after_rope_movement(rope, direction, count)
    return positions, rope[0], rope[1]


def tail_positions_after_rope_movement(rope, direction, count):
    """
    Durchführung einer Bewegungsfolge eine Seils beliebig vielen Knoten
    Rückgabe der besuchten Positionen des Endes
    """
    positions = [rope[-1]]
    for _ in range(count):
        rope[0] = move_one_step(rope[0], direction)
        for i in range(len(rope) - 1):
            rope[i + 1] = new_tail_after_close_gap(rope[i], rope[i + 1])
        positions.append(rope[-1])
    return positions, rope


def move_one_step(position, direction):
    """
    Durchführung eines Einzelschritts
    """
    match direction:
        case 'R':
            return position[0] + 1, position[1]
        case 'L':
            return position[0] - 1, position[1]
        case 'U':
            return position[0], position[1] - 1
        case 'D':
            return position[0] , position[1] + 1
    return position


if __name__ == '__main__':
    lines = read_puzzle("data/day9.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

