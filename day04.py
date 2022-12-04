from time import perf_counter as pfc


def read_puzzle(filename):
    with open(filename) as f:
        return [x for x in f]


def convert_to_tuples(lines):
    """
    ["2-4,6-8\n", "2-3,4-5\n"] -> [ [(2, 4), (6, 8)], [(2, 3), (4, 5)] ]
    """
    return list(map(lambda line: list(map(convert_to_tuple, line.strip().split(","))), lines))


def convert_to_tuple(line):
    """
    "1-2" -> (1,2)
    """
    return tuple(map(int, line.split("-")))


def is_containing(tuple1, tuple2):
    """
    Enthält eines der übergebenen Tupel das andere vollständig?
    """
    a, b = tuple1
    c, d = tuple2
    if a >= c and b <= d:
        return True
    if c >= a and d <= b:
        return True
    return False


def is_overlapping(tuple1, tuple2):
    """
    Überlappen sich die beiden übergebenen Tupel?
    """
    a, b = tuple1
    c, d = tuple2
    return b >= c and a <= d


def solve01(puzzle):
    """
    Anzahl der Paare, in denen in Tupel das andere vollständig enthält
    """
    return sum(map(lambda it: 1 if is_containing(it[0], it[1]) else 0, puzzle))


def solve02(puzzle):
    """
    Anzahl der überlappenden Paare
    """
    return sum(map(lambda it: 1 if is_overlapping(it[0], it[1]) else 0, puzzle))


if __name__ == '__main__':
    lines = read_puzzle("data/day4.txt")
    puzzle = convert_to_tuples(lines)
    start = pfc()
    print(solve01(puzzle), pfc()-start)
    start = pfc()
    print(solve02(puzzle), pfc()-start)

