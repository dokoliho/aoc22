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

    def get_borders(self):
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
        Ermitteln der Anzahl der von Wasser erreichbaren Oberflächenseiten
        Idee: Zunächst werden die "Luftwürfel" des Gebildes ermittelt
        Dabei wird auf allen Seiten ein "Luftfilm" um das Gebilde hinzugefügt
        Anschließend wird - beginnend an einer Ecke - die Luft geflutet und die
        erreichten Seiten gezählt
        """
        air_cubes, start_cube = self.create_air_cubes()
        return self.count_reachable_surface_sides(start_cube, air_cubes)

    def create_air_cubes(self):
        """
        Generieren der Liste der Luftwürfel und eines Startwürfels an einer Ecke
        """
        cubes = []
        x_min, x_max, y_min, y_max, z_min, z_max = self.get_borders()
        for x in range(x_min-1, x_max+2):
            for y in range(y_min-1, y_max+2):
                for z in range(z_min-1, z_max+2):
                    if (x, y, z) not in self.cubes:
                        cubes.append((x, y, z))
        return cubes, (x_min-1, y_min-1, z_min-1)

    def count_reachable_surface_sides(self, start_cube, air_cubes):
        """
        Fluten der Luft vom Startpunkt
        """
        q = [start_cube]
        reachable = 0
        while q:
            cube = q.pop(0)
            reachable += self.count_neighbours(cube)
            air_cubes.remove(cube)
            for next_cube in self.neighbours(cube):
                if next_cube in air_cubes and next_cube not in q:
                    q.append(next_cube)
        return reachable

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
