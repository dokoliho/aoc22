from functools import reduce
from typing import List
from collections import defaultdict
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


class Elf:
    """
    Repräsentation eines Elfen
    Attribute:
    row -> seine aktuelle Zeile
    col -> seine aktuelle Spalte
    proposal -> sein Vorschlag für das nächste Feld
    """

    """
    Liste der Bewegungsmöglichkeiten
    Je Richtung gibt es ein Tupel ("Liste der zu checkenden Felder", "Zielfeld")
    """
    seq = [
        ([(-1, -1), (-1, 0), (-1, 1)], (-1, 0)),  # NORTH
        ([(1, -1), (1, 0), (1, 1)], (1, 0)),  # SOUTH
        ([(-1, -1), (0, -1), (1, -1)], (0, -1)),  # WEST
        ([(-1, 1), (0, 1), (1, 1)], (0, 1)),  # EAST
    ]

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.proposal = None

    def is_lonely(self, plan):
        """
        Prüfung, ob es Nachbarn gibt
        """
        neighbours = [(row, col)
                      for row in range(self.row - 1, self.row + 2)
                      for col in range(self.col - 1, self.col + 2)
                      if (row, col) in plan.positions and (row, col) != (self.row, self.col)
                      ]
        return len(neighbours) == 0

    def generate_proposal(self, plan):
        """
        Berechnung eines Vorschlags gem. Vorgabe
        """
        self.proposal = None
        if not self.is_lonely(plan):
            for direction in range(4):
                self.proposal =  self.check_direction(plan, direction)
                if self.proposal is not None:
                    break
        return self.proposal

    def check_direction(self, plan, direction):
        """
        Check ob frei
        """
        test_cells, dest_cell = self.seq[(plan.first_direction + direction) % 4]
        all_free = all(((self.row + test[0], self.col + test[1]) not in plan.positions) for test in test_cells)
        return (self.row + dest_cell[0], self.col + dest_cell[1]) if all_free else None

    def move_to_proposal(self):
        self.row, self.col = self.proposal


class Plan:
    """
    Repräsentation der gesamten Karte
    Attribute:
    positions       -> Dictionary mit einer Position als Key und einem Elf-Objekt als Value
    proposals       -> Dictionary mit einer Position als Key und der Häufigkeit (int) als Value
    first_direction -> Offset für das Richtungsarray, wird bei jeder Runde aktualisiert
    """
    elves_count = 0

    def __init__(self):
        self.positions = {}
        self.proposals = None
        self.first_direction = 0

    def add_elf(self, elf: Elf):
        self.positions[(elf.row, elf.col)] = elf
        self.elves_count = self.elves_count + 1

    def remove_elf(self, elf: Elf):
        del self.positions[(elf.row, elf.col)]
        self.elves_count = self.elves_count - 1

    def do_round(self):
        self.generate_proposals()
        count = self.move_elves()
        self.first_direction = (self.first_direction + 1) % 4
        return count

    def generate_proposals(self):
        self.proposals = defaultdict(int)
        for elf in self.positions.values():
            if (proposal := elf.generate_proposal(self)) is not None:
                self.proposals[proposal] += 1
        return self.proposals.keys()

    def move_elves(self):
        count = 0
        keys = list(self.positions.keys())
        for key in keys:
            elf = self.positions[key]
            if elf.proposal and self.proposals[elf.proposal] == 1:
                self.remove_elf(elf)
                elf.move_to_proposal()
                self.add_elf(elf)
                count += 1
        return count


    def map_extensions(self):
        min_row = min(map(lambda tup: tup[0], self.positions))
        max_row = max(map(lambda tup: tup[0], self.positions))
        min_col = min(map(lambda tup: tup[1], self.positions))
        max_col = max(map(lambda tup: tup[1], self.positions))
        return min_row, max_row, min_col, max_col


    def empty_tiles(self):
        min_row, max_row, min_col, max_col = self.map_extensions()
        return (max_row-min_row+1) * (max_col-min_col+1) - self.elves_count

    def print_plan(self):
        min_row, max_row, min_col, max_col = self.map_extensions()
        print()
        for row in range(min_row-1, max_row+2):
            line = ""
            for col in range(min_col-1, max_col+2):
                line = line + ("#" if (row, col) in self.positions else ".")
            print(line)


def solve01(lines: List[str]) -> int:
    """
    Berechnung der freien Felder im Rechteck, das durch die Elfen nach 10
    Runden aufgespannt wird
    """
    plan = convert(lines)
    for _ in range(10):
        plan.do_round()
    return plan.empty_tiles()


def solve02(lines: List[str]) -> int:
    """
    Ermitteln der ersten Runde ohne Bewegung
    """
    count = 0
    plan = convert(lines)
    while True:
        count += 1
        if plan.do_round() == 0:
            plan.print_plan()
            return count


def convert(lines) -> Plan:
    """
    """
    plan = Plan()
    for row, line in enumerate(lines):
        for col in range(len(line)):
            if line[col] == "#":
                plan.add_elf(Elf(row, col))
    return plan


if __name__ == '__main__':
    lines = read_puzzle("data/day23.txt")
    start = pfc()
    print(solve01(lines), pfc() - start)
    start = pfc()
    print(solve02(lines), pfc() - start)
