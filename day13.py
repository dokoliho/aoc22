import copy
import functools
from typing import List
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    Ermitteln der Paare in der richtigen Reihenfolge
    Addieren deren Indizes
    """
    pairs = convert_to_packet_pairs(lines)
    return sum([i + 1 for i, p in enumerate(pairs) if check_order(p[0], p[1])])


def solve02(lines: List[str]) -> int:
    """
    Sortieren aller Packete inkl. zusätzlicher Divider
    Rückgabe des Produkts der Indizes der Divider
    """
    dividers = [[[2]], [[6]]]
    packets = convert_lines_to_packets(lines) + dividers
    packets = sorted(packets, key=functools.cmp_to_key(compare))
    return functools.reduce(lambda acc, tup: acc * (tup[0] + 1) if tup[1] in dividers else acc, enumerate(packets), 1)


def convert_to_packet_pairs(lines):
    """
    ['[1,1,3,1,1]\n', '[1,1,5,1,1]\n', '\n', '[[1],[2,3,4]]\n', '[[1],4]\n', '\n'] -->
    [ ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]), ([[1], [2, 3, 4]], [[1], 4])]
    """
    return list(map(lambda l: (convert_line_to_packet(l[0]), convert_line_to_packet(l[1])),
                    next_n_lines(lines, 2)))


def next_n_lines(lines, n):
    """
    Generator für das blockweise Einlesen der Eingabezeilen
    Gelesen werden immer n Zeilen und dann eine Leerzeile übersprungen
    """
    for i in range(0, len(lines), n + 1):
        yield lines[i:i + n]


def convert_lines_to_packets(lines):
    """
    Umwandeln aller Zeilen in Pakete
    Auslassen der Leerzeilen
    """
    return list(map(lambda fl: convert_line_to_packet(fl), filter(lambda line: len(line.strip()) > 0, lines)))


def convert_line_to_packet(line):
    """
    Parsen einer Eingabezeile
    Glücklicherweise hat sie bereits Python-Format, daher mit exec
    """
    loc = {}
    exec(f"packet = {line}", globals(), loc)
    return loc['packet']


def compare(packet1, packet2):
    """
    Vergleich zweier Pakete.
    Da check_order destruktiv ist, müssen vorher Kopien angefertigt werden, sonst sind die Pakete anschließend leer
    """
    p1 = copy.deepcopy(packet1)
    p2 = copy.deepcopy(packet2)
    check = check_order(p1, p2)
    if check:
        return -1
    if not check:
        return 1
    return 0


def check_order(packet1, packet2):
    """
    Vergleich zweier Pakete nach der vorgegebenen Logik
    Zunächst Behandlung des Falls, dass eines der Pakete leer ist
    Dann Vergleich der ersten Elemente
    """
    if len(packet1) == 0 or len(packet2) == 0:
        return empty_order(packet1, packet2)
    return check_first_element_order(packet1, packet2)


def check_first_element_order(packet1, packet2):
    """
    Vergleich der ersten Elemente zweier Pakete gem. vorgegebener Vorschriften
    Es wird eine dreiwertige Logik verwendet:
    True -> richtige Reihenfolge
    False -> falsche Reihenfolge
    None/Gleichheit -> rekursiver Aufruf von check_order mit jeweils um ein Element verkürzten Paketen
    """
    element1 = packet1.pop(0)
    element2 = packet2.pop(0)
    if isinstance(element1, int) and isinstance(element2, int):
        return int_order(element1, element2, packet1, packet2)
    result = list_order(element1, element2)
    if result is not None:
        return result
    return check_order(packet1, packet2)


def empty_order(packet1, packet2):
    """
    Behandlung des Falls, dass min. ein Paket leer ist.
    Es wird eine dreiwertige Logik verwendet:
    True -> richtige Reihenfolge
    False -> falsche Reihenfolge
    None -> keine Aussage möglich
    """
    if len(packet1) == 0 and len(packet2) == 0:
        return None
    if len(packet1) == 0:
        return True
    if len(packet2) == 0:
        return False


def int_order(element1, element2, packet1, packet2):
    """
    Reihenfolgeprüfung bei zwei Integern
    Bei Gleichheit müssen die Pakete weiter untersucht werden
    """
    if element1 == element2:
        return check_order(packet1, packet2)
    return element1 < element2


def list_order(packet1, packet2):
    """
    Reihenfolgeprüfung bei min. einer Liste
    Ggf. muss eine Seite in eine einelementige Liste überführt werden.
    """
    packet1 = ensure_list(packet1)
    packet2 = ensure_list(packet2)
    return check_order(packet1, packet2)


def ensure_list(element):
    """
    Einpacken eines Integers in eine Liste, falls nötig
    """
    return [element] if isinstance(element, int) else element


if __name__ == '__main__':
    lines = read_puzzle("data/day13.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

