from itertools import tee
from typing import List
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    Ermitteln, wieviel Sand fließen kann, bis er nach unten durchfällt
    """
    count = 0
    rocks = convert_to_rock_set(lines)
    sand = set()
    while not(pour_one_sand_unit((500, 0), rocks, sand)):
        count += 1
    return count


def solve02(lines: List[str]) -> int:
    """
    Bei einem festen Boden: Ermitteln, wieviel Sand fließen kann, bis die Quelle verstopft
    """
    count = 0
    rocks = convert_to_rock_set(lines)
    sand = set()
    while not(pour_one_sand_unit_with_bottom((500, 0), rocks, sand)):
        count += 1
    return count+1


def convert_to_rock_set(lines):
    """
    Umformen des Inputs in eine Liste mit den Positionen der Steine
    """
    waypoints = map(lambda l: list(map(lambda p: convert_to_tuple(p), l.strip().split("->"))), lines)
    result = set([])
    for line in waypoints:
        for pair in pairwise(line):
            result.update(set(draw_line(pair[0], pair[1])))
    return result


def convert_to_tuple(pair):
    """
    '500,30 '  ->  (500, 30)
    """
    l = pair.strip().split(",")
    return tuple(map(int, l))


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def pour_one_sand_unit(source, rocks, sand):
    """
    Simulation des Fallens eines Sandkorns
    Kein Boden
    Boolescher Rückgabewert signalisiert, ob das Korn endlos fällt.
    """
    fall_forever = False
    max_y = max(rocks, key=lambda r: r[1])[1]
    filled = rocks.union(sand)
    position = find_final_position(source, max_y, filled)
    if position[1] < max_y:
        sand.add(position)
    else:
        fall_forever = True
    return fall_forever


def pour_one_sand_unit_with_bottom(source, rocks, sand):
    """
    Simulation des Fallens eines Sandkorns
    Mit Boden
    Boolescher Rückgabewert signalisiert, ob das Korn bei der Quelle hängenbleibt.
    """
    filled = rocks.union(sand)
    bottom = max(rocks, key=lambda r: r[1])[1] + 2
    position = find_final_position(source, bottom-1, filled)
    sand.add(position)
    return source in sand


def find_final_position(position, max_y, filled):
    """
    Ermitteln der finalen Position eines Sandkorns bei gegebenen Startpunkt, der max. Falltiefe und der Belegung
    """
    while position[1] < max_y:
        candidates = [(position[0], position[1]+1), (position[0]-1, position[1]+1), (position[0]+1, position[1]+1)]
        new_position = next((candidate for candidate in candidates if candidate not in filled), None)
        if new_position is None: break
        position = new_position
    return position


def draw_line(source, destination):
    """
    Malen einer Linie zwischen zwei Punkten
    Rückgabe ist eine Liste der gemalten Punkte
    """
    if source[0] == destination[0]:
        return draw_vertical(source, destination)
    if source[1] == destination[1]:
        return draw_horizontal(source, destination)
    raise Exception("Diagonal line")


def draw_horizontal(source, destination):
    """
    Malen einer horizontalen Linie
    Rückgabe ist eine Liste der gemalten Punkte
    """
    x1 = min(source[0], destination[0])
    x2 = max(source[0], destination[0])
    return [(x, source[1]) for x in range(x1, x2+1)]


def draw_vertical(source, destination):
    """
    Malen einer vertikalen Linie
    Rückgabe ist eine Liste der gemalten Punkte
    """
    y1 = min(source[1], destination[1])
    y2 = max(source[1], destination[1])
    return [(source[0], y) for y in range(y1, y2+1)]


if __name__ == '__main__':
    lines = read_puzzle("data/day14.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

