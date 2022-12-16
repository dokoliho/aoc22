import math
import re
from typing import List
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


class Valve:
    """
    Klasse zur Repäsentation eines Ventils
    Attribute:
    name        -> Name des Ventils
    rate        -> Flussstärke, wenn das Ventil geöffnet ist
    neighbours  -> direkt erreichbare Nachbarventile
    distances   -> Map, die zu jedem anderen Ventil die Länge des kürzesten Wegs enthält
    """
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.neighbours = []
        self.distances = {}

    def __repr__(self):
        return self.name

    def set_neighbours(self, nodes, edges):
        """
        Eintragen der Nachbarn
        """
        for edge in get_edges_from_valve(edges, self.name):
            self.neighbours = self.neighbours + [get_valve_by_name(nodes, edge[1])]

    def set_distances(self):
        """
        Dijkstra zur Berechnung der Abstände zu den anderen Ventilen
        """
        discovered = []
        self.append_next_node(self, 0, discovered)
        while discovered:
            t = min(discovered, key=lambda tup: tup[0])
            discovered.remove(t)
            cost, node = t
            for next_node in node.neighbours:
                if next_node not in self.distances or self.distances[next_node] > cost + 1:
                    self.append_next_node(next_node, cost + 1, discovered)

    def append_next_node(self, next_node, cost, discovered):
        """
        Hilfsfunktion für Dijkstra
        Hinzufügen eines Zielventils mit (bisheriger) Mindestentfernung in die Border und
        die Map des Ausgangsventils (wird bei Verkürzung aktualisiert)
        """
        discovered.append((cost, next_node))
        self.distances[next_node] = cost


def convert_to_valves(lines):
    """
    Einlesen des Inputs
    Das Ventil-Dictionary wird in mehreren Durchgängen um Nachbarun und Entfernungen angereichert
    """
    valves = {}
    edges = []
    for line in lines:
        name, rate, destinations = convert_line_to_valve(line.strip())
        valves[name] = Valve(name, rate)
        edges = edges + list(map(lambda d: (name, d), destinations))
    for node in valves.values():
        node.set_neighbours(valves, edges)
    for node in valves.values():
        node.set_distances()
    return valves


def get_valve_by_name(valves, name):
    """
    Ermitteln eines Ventils mit gegebenen Namen
    """
    return valves[name]


def get_edges_from_valve(edges, valve_name):
    """
    Ermitteln aller Ausgangskanten zu einem Ventil
    """
    result = list(filter(lambda tup: tup[0] == valve_name, edges))
    return result


def get_start_node(nodes):
    """
    Hilfsmethode zur Identifikation des Startknoten
    """
    return get_valve_by_name(nodes, 'AA')


def convert_line_to_valve(line):
    """
    Konvertierung einer Input-Zeile in ein Tupel
    """
    m = re.search(r'Valve (\S+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)$', line)
    if m is None:
        raise Exception(f"No match with {line}")
    name, rate, destinations = m.groups()
    destinations = list(map(lambda d: d.strip(), destinations.split(",")))
    return name, int(rate), destinations


def sequence_generator(nodes_to_visit, nodes_visited, start_node, ttl=30):
    """
    Generator für die Erzeugung aller zulässigen Sequenzen
    Es wird nicht die volle ANzahl von 15! Sequenzen erzeugt, weil alle Knoten nicht in 30 Minuten besucht werden
    können.
    """
    for next_node in nodes_to_visit:
        duration = start_node.distances[next_node] + 1
        if duration <= ttl:
            yield from sequence_generator(nodes_to_visit - {next_node},
                                          nodes_visited + [next_node],
                                          next_node,
                                          ttl-duration)
    yield nodes_visited


def execute_seq(start_node, seq, ttl):
    """
    Berechnung des Release einer Sequenz
    """
    release = 0
    position = start_node
    for node in seq:
        duration = position.distances[node] + 1
        ttl -= duration
        release += ttl * node.rate
        position = node
    return release


def solve01(lines: List[str]) -> int:
    """
    Ermittlung des Maximums des Release bei einer vollständgen Enumeration aller in 30 Minuten zulässigen Sequenzen
    """
    nodes = convert_to_valves(lines)
    start_node = get_start_node(nodes)
    ttl = 30
    nodes_with_flow = {node for name, node in nodes.items() if node.rate > 0}
    seq_gen = sequence_generator(nodes_with_flow, [], start_node, ttl)
    result = -math.inf
    for seq in seq_gen:
        value = execute_seq(start_node, seq, ttl)
        result = max(result, value)
    return result


def solve02(lines: List[str]) -> int:
    """
    Berechnung, was mit zwei Prozessoren in 26 Minuten erreicht werden kann.
    Idee: Man lässt jeden Prozessor eine eigene Sequenz abarbeiten.
    Die Anzahl der unterschiedlichen Sequenzen in 26 Minuten ist mir 60k handhabbar.
    Für jede Sequenz kann berechnet werden, welcher Release durch sie erreicht wird.
    Die Sequenzen werden noch der Größe des Release sortiert.
    Dann wird sukzessive beginnend bei der besten Sequenz eine Sequenz ausgewählt und die
    zweite aus dem danach beginnenden Rest hinzugefügt. Davor muss nicht gesucht werden,
    weil diese Paarung bereits untersucht worden wäre.
    Die Paarung ist nur zulässig, wenn die Sequenzen disjunkt sind (ein Ventil kann nur einmal aufgemacht werden)
    Sofern die Paarung zulässig ist, werden die Releases zu einem Gesamtrelease addiert
    Falls ein neuer Maximalwert erreicht wird, wird dieser gemerkt
    Abbruch ist zulässig, wenn der Release der ersten (besseren) Sequenz schlechter ist als die Hälte des
    bisherigen Maximalwerts.
    Insgesamt funktioniert das nur, weil mit 15 relevanten Konten disjunkte Mengen in 26 Minuten produziert werden.
    """
    nodes = convert_to_valves(lines)
    start_node = get_start_node(nodes)
    ttl = 26
    nodes_with_flow = {node for name, node in nodes.items() if node.rate > 0}
    seq_gen = sequence_generator(nodes_with_flow, [], start_node, ttl)
    seq_and_release = list(map(lambda seq: (execute_seq(start_node, seq, ttl), seq), seq_gen))
    seq_and_release.sort(key=lambda tup: tup[0], reverse=True)

    best_release = 0
    for index, (release1, seq1) in enumerate(seq_and_release):
        if release1 * 2 < best_release:
            break
        for release2, seq2 in seq_and_release[index+1:]:
            if len(set(seq1 + seq2)) == len(seq1) + len(seq2):
                release = release1 + release2
                best_release = max(best_release, release)
    return best_release


if __name__ == '__main__':
    lines = read_puzzle("data/day16.txt")
    start = pfc()
    print(solve01(lines), pfc() - start)
    start = pfc()
    print(solve02(lines), pfc() - start)
