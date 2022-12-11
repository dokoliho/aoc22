from typing import List
import re
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    """
    return 0

def solve02(lines: List[str]) -> int:
    """
    """
    return 0



class Monkey:
    def __init__(self, lines):
        if len(lines) != 6:
            raise Exception("Lines count wrong")
        m = re.search(r"^Monkey (\d+):$", lines[0].strip())
        self.num = int(m.group(1))
        m = re.search(r"Starting items:(.+)$", lines[1].strip())
        self.items = list(map(int, m.group(1).split(",")))
        m = re.search(r"Operation:(.+)$", lines[2].strip())
        self.operation = m.group(1).strip()
        m = re.search(r"Test: divisible by (\d+)$", lines[3].strip())
        self.divisor = int(m.group(1))
        m = re.search(r"If true: throw to monkey (\d+)$", lines[4].strip())
        self.true_dest = int(m.group(1))
        m = re.search(r"If false: throw to monkey (\d+)$", lines[5].strip())
        self.false_dest = int(m.group(1))
        if self.true_dest == self.num or self.false_dest == self.num:
            raise Exception("Throwing to myself")
        self.count = 0

    def do_business(self, monkeys):
        while len(self.items) > 0:
            item = self.items.pop(0)
            self.count += 1 # one more inspection
            loc = {'old': item}
            exec(self.operation, globals(), loc)
            item = loc['new'] // 3
            if item % self.divisor == 0:
                monkeys[self.true_dest].items.append(item)
            else:
                monkeys[self.false_dest].items.append(item)


def convert(lines: List[str]) -> List[Monkey]:
    """
    """
    return list(map(lambda line_chunks: Monkey(line_chunks), next_n_lines(lines, 6)))


def next_n_lines(lines, n):
    beginn = 0
    while(True):
        end = min(beginn+n, len(lines))
        yield lines[beginn:end]
        beginn += (n+1)
        if beginn >= len(lines):
            break

if __name__ == '__main__':
    lines = read_puzzle("data/day11.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

