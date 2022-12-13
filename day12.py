import math
from itertools import chain
from typing import List
from time import perf_counter as pfc


def read_puzzle(filename: str) -> List[str]:
    with open(filename) as f:
        return [x for x in f]


def solve01(lines: List[str]) -> int:
    """
    Ermitteln des kürzesten Pfades von S zu E
    """
    matrix = convert_to_height_matrix(lines)
    edges = create_edges(matrix)
    return dijkstra(Node.source_node, Node.destination_node, edges)


def solve02(lines: List[str]) -> int:
    """
    Ermitteln des kürzesten Pfades aus der Menge aller Knoten mit Höhe 0 zum Knoten E
    Dies ist erstaunlicherweise schneller als solve01, weil nicht in aussichtslosen Löchern gesucht
    werden muss (die Verbindungen sind bei der Gegenrichtung reversibel, d.h. wohin ich absteigen kann,
    da komme ich auch wieder raus).
    """
    matrix = convert_to_height_matrix(lines)
    edges = revert_edges(create_edges(matrix))
    dijkstra(Node.destination_node, Node.source_node, edges)
    return min(map(lambda n: n.cost, starting_nodes(matrix)))


def convert_to_height_matrix(lines):
    """
    Anlegen der Knotenmatrix auf Basis der Inputdaten
    """
    return [[Node(row, col, c) for col, c in enumerate(line.strip())] for row, line in enumerate(lines)]


def reset_all_costs(matrix):
    """
    Setzen der Kosten für alle Knoten der Matrix auf unendlich
    """
    for line in matrix:
        for node in line:
            node.cost = math.inf


class Node:
    """
    Klasse für die Repräsentation eines Knoten
    Attribute:
    row         : Zeile der Matrix
    col         : Spalte der Matrix
    height      : Höhe an dieser Stelle
    cost        : Kosten für das Erreichen dieser Stelle
    Außederm gibt es noch die Klassenattribute:
    source_node         : Ausgangspunkt
    destination_node    : Ziel
    """

    source_node = None
    destination_node = None

    def __init__(self, row, col, char):
        """
        Konstruktor
        """
        self.row = row
        self.col = col
        self.height = self.get_height(char)
        self.cost = math.inf

    def get_height(self, char):
        """
        Ermitteln der Höhe.
        Bei den Sonderfällen 'S' und 'E' werden die Klassenattribute gesetzt
        """
        if char == 'S':
            char = 'a'
            Node.source_node = self
        if char == 'E':
            char = 'z'
            Node.destination_node = self
        return ord(char) - ord('a')

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Node({self.row}, {self.col}; Height: {self.height})"


class Edge:
    """
    Klasse für die Repräsentation einer Kante zwischen zwei Knoten
    """

    def __init__(self, source: Node, destination: Node):
        """
        Konstruktor
        """
        self.source = source
        self.destination = destination

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Edge({self.source.row}, {self.source.col} -> {self.destination.row}, {self.destination.col})"


def get_neighbours(matrix, row, col) -> List[Node]:
    """
    Ermitteln der max. 4 Nachbarknoten
    """
    result = []
    if row > 0:
        result.append(matrix[row-1][col])
    if col > 0:
        result.append(matrix[row][col-1])
    if row < len(matrix)-1:
        result.append(matrix[row+1][col])
    if col < len(matrix[0])-1:
        result.append(matrix[row][col+1])
    return result


def create_edges(matrix):
    """
    Ermitteln aller zulässigen Wege in der Matrix
    Es darf max. ein Höhenschritt nach oben ausgeführt werden
    """
    edges = []
    for row, line in enumerate(matrix):
        for col, node in enumerate(line):
            node : Node = matrix[row][col]
            neighbours = get_neighbours(matrix, row, col)
            for n in neighbours:
                if n.height <= node.height+1:
                    edges.append(Edge(node, n))
    return edges


def revert_edges(edges: List[Edge]):
    """
    "Umdrehen" aller Kanten für die Suche vom Endpunkt zu möglichen Startpunkten
    """
    return list(map(lambda e: Edge(e.destination, e.source), edges))


def dijkstra(source: Node, destination: Node, edges: List[Edge]):
    """
    Dijkstra-Algorithmus zum Ermitteln des kürzesten Pfades von source zu destination
    """
    source.cost = 0
    border = [source]
    while destination not in border:
        border = sorted(border, key=lambda n: n.cost)
        if len(border) == 0:
            break
        node = border.pop(0)
        for edge in edges:
            if edge.source == node:
                if edge.destination.cost > edge.source.cost + 1:
                    edge.destination.cost = edge.source.cost + 1
                    border.append(edge.destination)
    return destination.cost


def starting_nodes(matrix):
    """
    Ermitteln aller Knoten mit Höhe 0
    """
    return filter(lambda n: n.height == 0, chain.from_iterable(matrix))


if __name__ == '__main__':
    lines = read_puzzle("data/day12.txt")
    start = pfc()
    print(solve01(lines), pfc()-start)
    start = pfc()
    print(solve02(lines), pfc()-start)

