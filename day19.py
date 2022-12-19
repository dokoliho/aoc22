from typing import List, Tuple
import re
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]

class Blueprint():
    """
    Repräsentation für einen Blueprint
    """
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
    Summe der gewichteten besten Blueprint-Lösungen nach 24 Minuten
    """
    blueprints = convert(lines)
    stock = [0, 0, 0, 0]
    robots = [1, 0, 0, 0]
    sum = 0
    for bp in blueprints:
        sum += bp.num * apply_blueprint(bp, stock, robots, ttl=24)
    return sum


def solve02(lines: List[str]) -> int:
    """
    Produkt der besten Lösungen der ersten 3 Blueprints nach 32 Minuten
    """
    blueprints = convert(lines)
    stock = [0, 0, 0, 0]
    robots = [1, 0, 0, 0]
    prod = 1
    for bp in blueprints[:3]:
        prod *= apply_blueprint(bp, stock, robots, ttl=32)
    return prod


def convert(lines):
    """
    Anlage eines Blueprints mit der richtigen Nummer
    """
    result = []
    for line in lines:
        token = line.split(":")
        m = re.search(r"Blueprint (\d+)$", token[0])
        num = int(m.group(1))
        result.append(Blueprint(num, token[1]))
    return result


def apply_transition(transition, stock, robots):
    """
    Prüfen und ggf. Anwenden einer Transition auf eine gegebene Situation
    Zurückgegeben werden das Prüfergebnis und ggf. eine neue Situation
    """
    needed, produced = transition
    new_stock = [0, 0, 0, 0]
    for index, amount in enumerate(needed):
        if amount > stock[index]:
            return False, stock, robots
        new_stock[index] = stock[index] - amount
    new_robots = robots.copy()
    for index, amount in enumerate(produced):
        new_robots[index] += amount
    return True, new_stock, new_robots


def apply_blueprint(blueprint, stock, robots, ttl=24):
    """
    Nutzung eines Blueprints, um ausgehend von einer Startsituation die
    max. Anzahl von gecrackten Geodes zu produzieren
    Durchführung einer BFS, wobei unsinnige Transaktionen unterbunden werden
    """
    q = [(stock, robots, ttl)]
    max_geodes = 0
    while q:
        stock, robots, ttl = q.pop(0)
        if ttl == 0:
            max_geodes = max(max_geodes, stock[3])
            continue
        upper_bound = stock[3] + ttl * robots[3] + ttl * ttl
        if upper_bound < max_geodes:
            continue
        # Nur Produzieren durch die Roboter, keine Generierung von neuen Robotern
        new_stock = let_robots_work(stock, robots, blueprint.max_costs, ttl)
        q = append_new_situation(q, new_stock, robots, ttl)
        # Prüfen und ggf. Ausführen aller Transitionen des Blueprints
        for index, transition in enumerate(blueprint.transitions):
            # Es kann immer nur ein Robot produziert werden. D.h. es ist nicht sinnvoll,
            # Mmhr Robots  für ein Material zu bauen, als die teuerste Bauanlietung vorsieht
            # Ausnahme: Geode-Cracker (index == 3) machen immer Sinn
            if robots[index] >= blueprint.max_costs[index] and index != 3:
                continue
            # Die maximale Menge an Rohmaterial, das nach bis zum Ablauf der Zeit ausgegeben werden kann,
            # ergibt sich aus der Multiplikation der Restzeit und den höchsten Kosten für das Material
            # Es macht keinen Sinn, einen weiteren Robot für die Erzeugung dieses Materials zu bauen,
            # wenn wir bereits die max. Ausgabemenge erreicht haben. Ausnahme: Greode-Cracker
            if stock[index] >= blueprint.max_costs[index] * ttl and index != 3:
                continue
            applicable, new_stock, new_robots = apply_transition(transition, stock, robots)
            if applicable:
                # Falls die Transition anwendbar war, lassen wir noch die Robots (altes Setup!) arbeiten
                new_stock = let_robots_work(new_stock, robots, blueprint.max_costs, ttl)
                q = append_new_situation(q, new_stock, new_robots, ttl)
    return max_geodes


def let_robots_work(stock, robots, costs, ttl):
    """
    Alle Robots produzieren.
    Wenn im Ergebnis bei einem Material mehr vorhanden ist, als in der verbleibenden Zeit ausgegeben werden kann,
    dann wird die Menge dieses Materials auf die max. ausgebbare Menge reduziert. Das vermeidet das Wachstum
    des Backlogs in Bereiche, die nicht zielführend sind.
    """
    new_stock = stock.copy()
    for index in range(len(robots)):
        new_stock[index] += robots[index]
        if index < 3:
            new_stock[index] = min(new_stock[index], (ttl-1)*costs[index])
    return new_stock


def append_new_situation(queue, stock, robots, ttl):
    """
    Ehe eine neue Situation in die Queue aufgenommen wird, werden alle Einträge aus der Queue entfernt,
    die vom neuen Eintrag dominiert werden (also die in allen Ausprägungen schlechter oder bestenfalls gleich sind)
    """
    situation = (stock, robots, ttl - 1)
    queue = [s for s in queue if not is_superior(situation, s)]
    if situation not in queue:
        queue.append(situation)
    return queue


def is_superior(situation1, situation2):
    """
    Ermitteln, ob Situation 1 die Situation 2 dominiert.
    """
    stock1, robots1, ttl1 = situation1
    stock2, robots2, ttl2 = situation2
    stock1 = list(stock1)
    stock2 = list(stock2)
    for i in range(4):
        if ttl1 > ttl2:
            stock1[i] += (ttl1-ttl2) * robots1[i]
        else:
            stock2[i] += (ttl2-ttl1) * robots2[i]
        if stock2[i] > stock1[i] or robots2[i] > robots1[i]:
            return False
    return True


if __name__ == '__main__':
    lines = read_puzzle("data/day19.txt")
    start = pfc()
    print(solve01(lines), pfc() - start)
    start = pfc()
    print(solve02(lines), pfc() - start)
