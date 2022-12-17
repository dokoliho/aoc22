from copy import copy
from dataclasses import dataclass
from typing import List, Tuple
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


@dataclass
class Sprite:
    """
    Klasse zur Repräsentation eines Sprites
    """
    top: int                    # Y-Position der obersten Pixel
    left: int                   # X-Position der am weitesten links stehenden Pixel
    shape: List[Tuple]          # Liste von Punkten/Tupel, die das Aussehen des Sprites wiedergeben

    def get_bottom(self):
        return self.top - max(self.shape, key=lambda tup: tup[1])[1]

    def get_height(self):
        return max(self.shape, key=lambda tup: tup[1])[1] + 1

    def get_right(self):
        return self.left + max(self.shape, key=lambda tup: tup[0])[0]


class Chamber:
    """
    Klasse zur Repäsentation der Höhlenkammer
    """
    def __init__(self, width: int):
        self.width = width
        self.rocks = []

    def get_height(self):
        if self.rocks:
            return max(self.rocks, key=lambda tup: tup[1])[1]+1
        return 0

    def get_height_in_col(self, col):
        rocks = list(filter(lambda tup: tup[0] == col, self.rocks))
        if rocks:
            return max(rocks, key=lambda tup: tup[1])[1]
        return 0

    def collide(self, sprite: Sprite):
        """
        Feststellen, ob ein Sprite mir der Grundlinie oder einem bereits fixierten Sprite kollidiert
        """
        if sprite.get_bottom() < 0:
            return True
        if sprite.left < 0:
            return True
        if sprite.get_right() >= self.width:
            return True
        for rock in sprite.shape:
            current_rock = (sprite.left + rock[0], sprite.top - rock[1])
            if current_rock in self.rocks:
                return True
        return False

    def freeze(self, sprite):
        """
        Festsetzen des Sprites an der aktuellen Position
        Die Pixel des Sprites werden dauerhafte Blockaden
        """
        for rock in sprite.shape:
            current_rock = (sprite.left + rock[0], sprite.top - rock[1])
            self.rocks.append(current_rock)
        # Entfernen von Blockaden, die 30 Zeilen unterhalb liegen. Die 30
        # ergibt sich aus Versuchen
        heights = [self.get_height_in_col(col) for col in range(self.width)]
        new_rocks = list(filter(lambda r: r[1] > heights[r[0]] - 30, self.rocks))
        self.rocks = new_rocks


"""
Sprites unterschiedlichen Aussehens mit Ihren Startpositionen
"""
dash_shape = [(i, 0) for i in range(4)]
plus_shape = [(1, i) for i in range(3)] + [(0, 1), (2, 1)]
l_shape = [(2, i) for i in range(3)] + [(j, 2) for j in range(2)]
line_shape = [(0, i) for i in range(4)]
block_shape = [(i, j) for i in range(2) for j in range(2)]


def sequence_of_sprites(chamber: Chamber):
    """
    Generator für Sprites
    """
    while True:
        yield Sprite(chamber.get_height()+3, 2, dash_shape)
        yield Sprite(chamber.get_height()+5, 2, plus_shape)
        yield Sprite(chamber.get_height()+5, 2, l_shape)
        yield Sprite(chamber.get_height()+6, 2, line_shape)
        yield Sprite(chamber.get_height()+4, 2, block_shape)


def sequence_of_jet(pattern: str):
    """
    Generator für Jet-Richtungen
    """
    index = 0
    while True:
        yield pattern[index]
        index = (index + 1) % len(pattern)


def solve01(lines: List[str]) -> int:
    """
    Simulation von 2022 follenden Sprites
    """
    chamber = Chamber(7)
    let_some_fall(chamber, lines[0].strip(), 2022)
    return chamber.get_height()


def solve02(lines: List[str]) -> int:
    """
    Vermutung: Es gibt Zyklen beim Zuwachs der Höhe
    Lösungsidee: Ermitteln der Zuwachswerte für 5000 fallende Sprites
    Suche nach einem möglichst langen Zyklus bei den Zuwachswerten (Zyklus muss nicht beim ersten Sprite beginnen)
    Ermittlung des Zuwachs für den gesamten Zyklus
    Die Höhe ergibt sich aus dem Zuwachs vor dem ersten Zyklus, n mal dem Zykluszuwachs und dem Restzuwachs
    nach dem letzten Zyklus
    """
    chamber = Chamber(7)
    iterations = 1000000000000
    (start_cycle, cycle_len), increases = find_cycle(chamber, lines[0].strip(), 5000)
    increase = sum(increases[:start_cycle])                                     # Zuwachs vor dem ersten Zyklus
    cycle_increase = sum(increases[start_cycle:(start_cycle+cycle_len)])        # Zuwachs bei einem Zyklus
    num_cycles = (iterations - start_cycle) // cycle_len                        # Anzahl der ganzen Zyklen
    increase += num_cycles * cycle_increase
    remaining_iterations = (iterations - start_cycle) % cycle_len
    increase += sum(increases[start_cycle:(start_cycle+remaining_iterations)])  # Zuwachs nach dem letzen Zyklus
    return increase


def let_some_fall(chamber: Chamber, jet_pattern: str, count: int):
    """
    Simulation mehrerer fallender Sprites
    """
    sprite_seq = sequence_of_sprites(chamber)
    jet_seq = sequence_of_jet(jet_pattern)
    for i in range(count):
        let_one_fall(chamber, sprite_seq, jet_seq)


def find_cycle(chamber: Chamber, jet_pattern: str, count: int):
    """
    Simulation mehrerer fallender Sprites und Suche nach einem möglichst langen Zyklus beim
    Höhemzuwachs
    """
    sprite_seq = sequence_of_sprites(chamber)
    jet_seq = sequence_of_jet(jet_pattern)
    increases = list(map(lambda i: let_one_fall(chamber, sprite_seq, jet_seq), range(count)))
    cycles = []
    for start_cycle in range(len(increases)):
        for cycle_len in range((len(increases)-start_cycle)//2//5*5, 1, -5):
            if increases[start_cycle:(start_cycle+cycle_len)] != \
                    increases[(start_cycle+cycle_len):(start_cycle+2*cycle_len)]:
                continue
            cycles.append((start_cycle, cycle_len))
    return sorted(cycles, key=lambda tup: tup[1]*100-tup[0], reverse=True)[0], increases


def let_one_fall(chamber: Chamber, sprite_seq, jet_seq):
    """
    Simulation eines Sprites
    Rückgabewert ist der Höhenzuwachs durch den Sprite
    """
    sprite = next(sprite_seq)
    start_height = chamber.get_height()
    while True:
        # Seitwärtsbewegung
        next_sprite = moved_sprite(sprite, jet_seq)
        if not chamber.collide(next_sprite):
            sprite = next_sprite
        # Abwärtsbewegung
        next_sprite = copy(sprite)
        next_sprite.top = next_sprite.top - 1
        if chamber.collide(next_sprite):
            chamber.freeze(sprite)
            return chamber.get_height() - start_height
        sprite = next_sprite


def moved_sprite(sprite: Sprite, jet_seq):
    """
    Seitwärtsbewegung des Sprites
    """
    jet = next(jet_seq)
    next_sprite = copy(sprite)
    if jet == '<':
        next_sprite.left = next_sprite.left - 1
    if jet == '>':
        next_sprite.left = next_sprite.left + 1
    return next_sprite


if __name__ == '__main__':
    lines = read_puzzle("data/day17.txt")
    start = pfc()
    print(solve01(lines), pfc() - start)
    start = pfc()
    print(solve02(lines), pfc() - start)
