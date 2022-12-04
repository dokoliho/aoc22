from functools import reduce
from itertools import islice
from time import perf_counter as pfc


def read_puzzle(filename):
    with open(filename) as f:
        return [x for x in f]


def convert_to_priority_lists(puzzle):
    """
    Zerlegen der Strings in Listen von Charakters (äußere map)
    Überführen der Charakter in Prioritäten (innere map)
    """
    return list(map(lambda line: list(map(priority, line.strip())), puzzle))


def priority(item):
    """
    Umrechnung Character -> Priorität
    """
    if item.islower():
        return ord(item) - ord('a') + 1
    else:
        return ord(item) - ord('A') + 27


def solve1(puzzle):
    """
    Lösung Teil eins: Aufsummeren der Prioritäten der doppelten Elemente in den beiden
    Abteilungen des Rucksacks
    """
    return sum(map(find_common_item_in_rucksack, puzzle))


def find_common_item_in_rucksack(rucksack):
    """
    Aufteilen des Rucksacks in zwei Abteilungen
    Ermitteln des gemeinsamen Elements
    """
    length = len(rucksack)
    middle_index = length // 2
    return find_common_item_in_lists([rucksack[:middle_index], rucksack[middle_index:]])


def find_common_item_in_lists(lists):
    """
    Ermitteln der gemeinsamen Elemente in mehreren Listen
    """
    iset = reduce(lambda a, b: set(a).intersection(set(b)), lists)
    return iset.pop() if len(iset) > 0 else None


def solve2(puzzle):
    """
    Durchlaufen der Rucksäcke in 3-er Gruppen
    Ermitteln des gemeinsamen Elements
    Aufaddieren
    """
    window_size = 3
    return reduce(lambda value, element: value + find_common_item_in_lists(element), batched(puzzle, window_size), 0)


def batched(iterable, n):
    """
    Erzeugung eines Generators, der das Iterable in Abschnitten zurückliefert.
    Die übergebene Sequenz wird mit Hilfe eines Iterators durchlaufen
    islice holt n Elemente (bei einer Liste immer die ersten, bei einem Iterator aufeinanderfolgende)

    Beim ersten Aufruf des Generators wird er wie eine Funktion ausgeführt, wobei sich yield wie return verhält.
    Bei jedem weiteren Aufruf wird der Generator nach dem letzten yield fortgesetzt.
    """
    it = iter(iterable)
    while batch := list(islice(it, n)):
        yield batch


def solve(puzzle):
    puzzle = convert_to_priority_lists(puzzle)
    return solve2(puzzle)


if __name__ == '__main__':
    puzzle = read_puzzle("data/day3.txt")
    start = pfc()
    print(solve(puzzle), pfc()-start)

