from time import perf_counter as pfc

def read_puzzle(filename):
    with open(filename) as f:
        return [int(x) for x in f]


def solve(puzzle):
    return None


if __name__ == '__main__':
    puzzle = read_puzzle("data/day2.txt")
    start = pfc()
    print(solve(puzzle), pfc()-start)