import math
from copy import copy
from functools import reduce
from typing import List
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


class Elf:

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
        count = 0
        for row in range(self.row-1, self.row+2):
            for col in range(self.col-1, self.col+2):
                if (row, col) in plan.positions:
                    count += 1
        return count <= 1

    def generate_proposal(self, plan):
        self.proposal = None
        if not self.is_lonely(plan):
            for direction in range(4):
                test_cells, dest_cell = self.seq[(plan.first_direction + direction) % 4]
                if reduce(
                        lambda acc, test: acc and (self.row + test[0], self.col + test[1]) not in plan.positions,
                        test_cells,
                        True):
                    self.proposal = (self.row + dest_cell[0], self.col + dest_cell[1])
                    break
        return self.proposal

class Plan:

    elves_count = 0

    def __init__(self):
        self.positions = {}
        self.proposals = {}
        self.first_direction = 0

    def add_elf(self, elf: Elf):
        self.positions[(elf.row, elf.col)] = elf
        self.elves_count = self.elves_count + 1

    def do_round(self):
        self.generate_proposals()
        count = self.move_elves()
        self.first_direction = (self.first_direction + 1) % 4
        return count

    def generate_proposals(self):
        self.proposals = {}
        for elf in self.positions.values():
            proposal = elf.generate_proposal(self)
            if proposal:
                if proposal in self.proposals:
                    self.proposals[proposal] += 1
                else:
                    self.proposals[proposal] = 1
        return self.proposals.keys()

    def move_elves(self):
        count = 0
        keys = list(self.positions.keys())
        for key in keys:
            elf = self.positions[key]
            if elf.proposal and self.proposals[elf.proposal] == 1:
                del self.positions[key]
                elf.row = elf.proposal[0]
                elf.col = elf.proposal[1]
                self.positions[(elf.row, elf.col)] = elf
                count += 1
        return count

    def empty_tiles(self):
        min_row = min(map(lambda tup: tup[0], self.positions))
        max_row = max(map(lambda tup: tup[0], self.positions))
        min_col = min(map(lambda tup: tup[1], self.positions))
        max_col = max(map(lambda tup: tup[1], self.positions))
        return (max_row-min_row+1) * (max_col-min_col+1) - self.elves_count

    def print_plan(self):
        min_row = min(map(lambda tup: tup[0], self.positions))
        max_row = max(map(lambda tup: tup[0], self.positions))
        min_col = min(map(lambda tup: tup[1], self.positions))
        max_col = max(map(lambda tup: tup[1], self.positions))
        print()
        for row in range(min_row-1, max_row+1):
            line = ""
            for col in range(min_col-1, max_col+1):
                line = line + ("#" if (row, col) in self.positions else ".")
            print(line)




def solve01(lines: List[str]) -> int:
    """
    """
    plan = convert(lines)
    for _ in range(10):
        plan.do_round()
    return plan.empty_tiles()


def solve02(lines: List[str]) -> int:
    """
    """
    count = 0
    plan = convert(lines)
    while True:
        count += 1
        if plan.do_round() == 0:
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
    side2 = pfc()
    print(solve01(lines), pfc() - side2)
    side2 = pfc()
    print(solve02(lines), pfc() - side2)
