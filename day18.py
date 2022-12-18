from typing import List, Tuple
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


class Shape:
    """
    Repräsentation des Gesamtgebildes
    Attribute:
    cubes       -> Liste von 3D-Tupeln, die die gescannten Würfel repräsentieren
    surface     -> Oberfläche des Gebildes (inkl. Einschlüsse)
    """
    def __init__(self):
        self.cubes = []
        self.air_cubes = None
        self.surface = 0

    def add_cube(self, cube):
        """
        Hinzufügen eines Scans
        Oberfläche wird aktualisiert: Alle Nachbarn verlieren eine Seite; dazu kommen die 6 Seiten des
        neuen Würfels abzüglich der Seiten mit Nachbarn
        """
        count = self.count_neighbours(cube)
        self.cubes.append(cube)
        self.surface = self.surface + 6 - 2*count

    def count_neighbours(self, cube):
        """
        Ermitteln der Anzahl der benachbarten Würfelfelder, die durch das Gebilde belegt sind
        """
        return len(list(filter(lambda c: c in self.cubes, self.neighbours(cube))))

    def get_hull(self):
        """
        Abmessungen des Gebildes
        -> x_min, x_max, y_min, y_max, z_min, z_max
        """
        result = []
        for dim in range(3):
            result.append(min(map(lambda tup: tup[dim], self.cubes)))
            result.append(max(map(lambda tup: tup[dim], self.cubes)))
        return tuple(result)

    def reachable_surface(self):
        """
        Fluten der Luft von außen mittels Breitensuche
        Jede getroffene Seite wird aufaddiert
        """
        flooded = []
        reachable = 0
        hull = self.get_hull()
        x_min, x_max, y_min, y_max, z_min, z_max = hull
        q = [(x_min-1, y_min-1, z_min-1)]
        while q:
            cube = q.pop(0)
            flooded.append(cube)
            for next_cube in self.neighbours(cube):
                if not self.is_in_hull(next_cube, hull):
                    continue
                if next_cube in q or next_cube in flooded:
                    continue
                if next_cube in self.cubes:
                    reachable += 1
                    continue
                q.append(next_cube)
        return reachable

    def is_in_hull(self, cube, hull):
        """
        Überprüfen, ob sich der Würfel noch in der Hülle + 1 befindet
        """
        x, y, z = cube
        x_min, x_max, y_min, y_max, z_min, z_max = hull
        return x_min-1 <= x <= x_max+1 and y_min-1 <= y <= y_max+1 and z_min-1 <= z <= z_max+1

    def neighbours(self, cube):
        """
        Ermitteln der geometrischen 6 Nachbarwürfel
        """
        x, y, z = cube
        return [(x-1, y, z), (x+1, y, z), (x, y-1, z), (x, y+1, z), (x, y, z-1), (x, y, z+1)]


def solve01(lines: List[str]) -> int:
    """
    Ermitteln der Oberfläche des Gebildes, das sich aus den gescannten Cubes ergibt
    """
    cubes = convert(lines)
    shape = Shape()
    for cube in cubes:
        shape.add_cube(cube)
    return shape.surface


def solve02(lines: List[str]) -> int:
    """
    Ermitteln der Oberfläche des Gebildes, die von Wasser erreicht werden kann
    """
    cubes = convert(lines)
    shape = Shape()
    for cube in cubes:
        shape.add_cube(cube)
    return shape.reachable_surface()


def convert(lines):
    """
    ['2,2,2\n', '1,2,2\n'] ->
    [(2, 2, 2), (1, 2, 2)]
    """
    return list(map(lambda line: tuple(map(int, line.strip().split(","))), lines))


if __name__ == '__main__':
    lines = read_puzzle("data/day18.txt")
    start = pfc()
    print(solve01(lines), pfc() - start)
    start = pfc()
    print(solve02(lines), pfc() - start)
