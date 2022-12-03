from functools import reduce
from time import perf_counter as pfc


def read_puzzle(filename):
    with open(filename) as f:
        return [x for x in f]


def convert_to_priority_lists(puzzle):
    return list(map(lambda it1: list(map(lambda it2: priority(it2), list(it1.strip()))), puzzle))


def priority(item):
    if item.islower():
        return ord(item) - ord('a') + 1
    else:
        return ord(item) - ord('A') + 27


def solve1(puzzle):
    return sum(list(map(find_common_item_in_rucksack, puzzle)))


def find_common_item_in_rucksack(rucksack):
    length = len(rucksack)
    middle_index = length // 2
    return find_common_item_in_lists([rucksack[:middle_index], rucksack[middle_index:]])


def find_common_item_in_lists(lists):
    iset = reduce(lambda a, b: set(a).intersection(set(b)), lists)
    return iset.pop() if len(iset) > 0 else None


def solve2(puzzle):
    window_size = 3
    sum = 0
    for i in range(0, len(puzzle) - window_size + 1, window_size):
        window = puzzle[i: i + window_size]
        sum += find_common_item_in_lists(window)
    return sum


def solve(puzzle):
    puzzle = convert_to_priority_lists(puzzle)
    return solve2(puzzle)


if __name__ == '__main__':
    puzzle = read_puzzle("data/day3.txt")
    start = pfc()
    print(solve(puzzle), pfc()-start)