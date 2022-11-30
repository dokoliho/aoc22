from time import perf_counter as pfc

def read_puzzle(filename):
    with open(filename) as f:
        return [int(x) for x in f]


def solve(puzzle):
    pass


puzzle = read_puzzle("data/Tag_01.txt")
start = pfc()
print(solve(puzzle), pfc()-start)