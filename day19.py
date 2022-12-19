from typing import List, Tuple
import re
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]

class Blueprint():

    def __init__(self, num, line):
        self.num = num
        self.transitions = []
        m = re.search(r"Each ore robot costs (\d+) ore.", line)
        ore = int(m.group(1))
        self.transitions.append(((ore, 0, 0, 0), (1, 0, 0, 0)))
        m = re.search(r"Each clay robot costs (\d+) ore.", line)
        ore = int(m.group(1))
        self.transitions.append(((ore, 0, 0, 0), (0, 1, 0, 0)))
        m = re.search(r"Each obsidian robot costs (\d+) ore and (\d+) clay.", line)
        ore = int(m.group(1))
        clay = int(m.group(2))
        self.transitions.append(((ore, clay, 0, 0), (0, 0, 1, 0)))
        m = re.search(r"Each geode robot costs (\d+) ore and (\d+) obsidian.", line)
        ore = int(m.group(1))
        obsidian = int(m.group(2))
        self.transitions.append(((ore, 0, obsidian, 0), (0, 0, 0, 1)))
        costs = list(map(lambda tup: tup[0], self.transitions))
        self.max_costs = (
            max(costs, key=lambda tup: tup[0])[0],
            max(costs, key=lambda tup: tup[1])[1],
            max(costs, key=lambda tup: tup[2])[2],
            max(costs, key=lambda tup: tup[3])[3],
        )


def solve01(lines: List[str]) -> int:
    """
    """
    return 0


def solve02(lines: List[str]) -> int:
    """
    """
    return 0


def convert(lines):
    """
    """
    result = []
    for line in lines:
        token = line.split(":")
        m = re.search(r"Blueprint (\d+)$", token[0])
        num = int(m.group(1))
        result.append(Blueprint(num, token[1]))
    return result


def apply_transition(transition, stock, robots):
    needed, produced = transition
    new_stock = []
    for index, amount in enumerate(needed):
        if amount > stock[index]:
            return False, stock, robots
        new_stock.append(stock[index] - amount)
    new_robots = list(robots)
    for index, amount in enumerate(produced):
        new_robots[index] += amount
    return True, tuple(new_stock), tuple(new_robots)


def apply_blueprint(blueprint, stock, robots, ttl=24):
    q = [(stock, robots, ttl)]
    max_geodes = 0
    while q:
        print(f"* {q}", flush=True)
        stock, robots, ttl = q.pop(0)
        if ttl == 0:
            max_geodes = max(max_geodes, stock[3])
            continue
        new_stock = let_robots_work(stock, robots, blueprint.max_costs, ttl)
        append_new_situation(q, new_stock, robots, ttl)
        for index, transition in enumerate(blueprint.transitions):
            if robots[index] >= blueprint.max_costs[index] and index != 3:
                continue        #    Nicht mehr Robots als die Kosten des teuersten Robots
            if stock[index] > blueprint.max_costs[index] * ttl and index != 3:
                continue        #    Nicht mehr Robots für etwas, das wir nicht mehr ausgeben können
            applicable, new_stock, new_robots = apply_transition(transition, stock, robots)
            if applicable:
                let_robots_work(stock, robots, blueprint.max_costs, ttl)
                append_new_situation(q, new_stock, new_robots, ttl)
    return max_geodes


def let_robots_work(stock, robots, costs, ttl):
    new_stock = list(stock)
    for index, amount in enumerate(robots):
        new_stock[index] += amount
        if index != 3:
            new_stock[index] = min(new_stock[index], (ttl-1)*costs[index])
    return tuple(new_stock)


def append_new_situation(queue, stock, robots, ttl):
    situation = (stock, robots, ttl - 1)
    if not situation in queue:
        queue.append(situation)


if __name__ == '__main__':
    lines = read_puzzle("data/day19.txt")
    start = pfc()
    print(solve01(lines), pfc() - start)
    start = pfc()
    print(solve02(lines), pfc() - start)
